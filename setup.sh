# Print system environment variables
echo "JAVA_HOME: $JAVA_HOME"
echo "PATH: $PATH"

# Install sdkman
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install Java Development Kit (JDK)
sdk install java

# Set Java environment variables
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"
export PATH="$JAVA_HOME/bin:$PATH"

# Print updated system environment variables
echo "JAVA_HOME: $JAVA_HOME"
echo "PATH: $PATH"

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
pip install --upgrade tabula-py
