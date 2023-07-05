# Install sdkman
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install Java
sdk install java

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
