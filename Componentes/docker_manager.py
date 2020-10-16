from time import sleep

import docker


class DockerManager:

  def __init__(self):
    "High-level API"
    self.cli = docker.from_env()
    
    "Low-level docker API"
    self.api_cli = docker.APIClient(base_url='unix://var/run/docker.sock')
    
    "Default host config for containers"
    self.client_container_config = self.api_cli.create_host_config( privileged=True, cap_add=['NET_ADMIN'] )

  def create_client_container(self, container_name):
    """
      Creates and starts a client container

      Args:
        container_name (str): name of the container
      
      Returns:
        str IP address of the container
    """
    try:
      ctnr = self.api_cli.create_container('renanalves/android-22:v2', 
        command='/root/port_forward.sh', 
        detach=True, tty=True, 
        name=container_name, 
        host_config=self.client_container_config )

      self.api_cli.start( container=ctnr.get('Id') )
    except:
      return None

    """Wait container start to get the IP"""
    while True:
      container = self.cli.containers.get(container_name)

      if container.status == 'running':
        return container.attrs.get('NetworkSettings').get('IPAddress')
      
      sleep(1)


docker_mgr = DockerManager()
