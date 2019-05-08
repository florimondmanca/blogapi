"""Application definition."""
from bocadillo import App, discover_providers

app = App()
discover_providers("blogapi.providerconf")

# Create routes here.