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
      ctnr = self.api_cli.create_container( 'renanalves/android-22:v2', 
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
  
  def create_server_container(self, container_name, memory, bind_ports):
    try:
      if bind_ports:
        self.cli.containers.run(
          'renanalves/server-testbed:configured',
          name=container_name,
          detach=True, 
          tty=True, 
          mem_limit=memory,
          ports={
            '30015/tcp': 30015,
            '31000/tcp': 31000,
            '36114/tcp': 36114,
            '36381/tcp': 36381,
            '36415/tcp': 36415,
            '36241/tcp': 36241,
            '40000/tcp': 40000,
            '40001/tcp': 40001,
            '40005/tcp': 40005,
            '40006/tcp': 40006,
            '40010/tcp': 40010,
            '40011/tcp': 40011,
            '40020/tcp': 40020,
            '36619/tcp': 36619
          }
        )
      else:
        self.cli.containers.run(
          'renanalves/server-testbed:configured',
          name=container_name,
          detach=True, 
          tty=True, 
          mem_limit=memory
        )
    except:
      return None
    
    return True


docker_mgr = DockerManager()
