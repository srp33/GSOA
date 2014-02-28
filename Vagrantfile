$script = <<SCRIPT
if [ ! -d gsoa ]
then
  sudo apt-get install -y git

  cd /home/vagrant
  git clone https://srp33@bitbucket.org/srp33/gsoa.git
  sudo chmod 777 gsoa -R
  mv gsoa/* .
  mv gsoa/.git .
  rm -rf gsoa

  ./initialize_vm
fi
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision :shell, :inline => $script

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "16384"]
    vb.customize ["modifyvm", :id, "--cpus", "16"]
  end
end
