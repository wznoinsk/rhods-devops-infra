cat <<EOF | tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
EOF
microdnf install -y git shadow-utils findutils python3.12 kubectl jq skopeo

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

