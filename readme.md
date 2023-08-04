This project is a connector for Streamlit for Qdrant.

# secrets.toml

This project requires a `secrets.toml` file in the top level directory of the project for storing the Qdrant `url` and `api_key`.

The structure of the `secrets.toml` should be as follows:

```toml
[connections.qdrant]
url = "string"
api_key = "string"
```