import os
from dotenv import load_dotenv
import airbyte as ab

load_dotenv()
os.environ["AIRBYTE_ENABLE_UNSAFE_CODE"] = "true"

# Workaround for CDK bug: ConcurrentDeclarativeSource.configure() does
# `self._config or config`, which drops the user config when the executor
# injects custom Python components (__injected_components_py). Fix: merge
# injected keys into the user config so both survive validation and runtime.
from airbyte_cdk.connector import DefaultConnectorMixin
from airbyte_cdk.sources.declarative.concurrent_declarative_source import ConcurrentDeclarativeSource

def _patched_configure(self, config, temp_dir):
    # CDK bug: original does `self._config or config`, discarding user config when
    # injected_components_py makes self._config truthy. Merge instead, and update
    # self._config so that streams() (which reads self._config directly) also sees
    # the user fields.
    merged = {**config, **(self._config or {})}
    self._config = merged
    return DefaultConnectorMixin.configure(self, merged, temp_dir)

ConcurrentDeclarativeSource.configure = _patched_configure

source = ab.get_source(
    "source-google-analytics-data-api",
    install_if_missing=False,
    config={
        "property_ids": [os.environ["GA4_PROPERTY_ID"]],
        "credentials": {
            "auth_type": "Client",
            "client_id": os.environ["GA4_CLIENT_ID"],
            "client_secret": os.environ["GA4_CLIENT_SECRET"],
            "refresh_token": os.environ["GA4_REFRESH_TOKEN"],
            "access_token": os.environ["GA4_ACCESS_TOKEN"],
        },
        "date_ranges_start_date": os.environ.get("GA4_START_DATE", "2025-01-01"),
        "date_ranges_end_date": os.environ.get("GA4_END_DATE", "2025-01-02"),
    },
)

print("Checking connection...")
source.check()

print("\nAvailable streams:")
streams = source.get_available_streams()
for s in streams:
    print(f"  - {s}")

# Read a single stream into a DataFrame
TARGET_STREAM = "daily_active_users"

print(f"\nReading stream: {TARGET_STREAM}")
source.select_streams([TARGET_STREAM])
result = source.read()

df = result[TARGET_STREAM].to_pandas()
print(f"\nRows: {len(df)}")
print(df.head(10))
