# Update package lists
apt update

# Install Java
apt install -y default-jdk

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
