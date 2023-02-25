# FASTAPI Tutorial

This is a simple example FastAPI application that pretends to be a TodoApi.

# Deploying on AWS
Log into your AWS account and create an EC2 instance (`t2.micro`), using the latest stable
Ubuntu Linux AMI.

[SSH into the instance](https://aws.amazon.com/blogs/compute/new-using-amazon-ec2-instance-connect-for-ssh-access-to-your-ec2-instances/) and run these commands to update the software repository and install
our dependencies.

```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```

Clone the FastAPI server app.

```bash
git clone https://github.com/JoelEmmanuelCloud/deploy-a-todoapi-on-AWS.git
```

Add the FastAPI configuration to NGINX's folder. Create a file called `fastapi_nginx`.

```bash
sudo nano /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):

```
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```


Start NGINX.

```bash
sudo service nginx restart
```

Start FastAPI.

```bash
cd fastapi-tutorial
python3 -m uvicorn todo:app
```

Update EC2 security-group settings for your instance to allow HTTP traffic to port 80.

Now when you visit your public IP of the instance, you should be able to access your API.
