Setup
```
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source "$HOME/.local/bin/env"
```

Run
```
uv run get_related_uids_in_subnet.py
```