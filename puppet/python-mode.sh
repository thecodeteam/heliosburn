
# Install Pathogen
if [ ! -d "/home/vagrant/.vim/autoload" ]; then
  mkdir -p /home/vagrant/.vim/autoload
fi

if [ ! -d "/home/vagrant/.vim/bundle" ]; then
  mkdir -p /home/vagrant/.vim/bundle
fi

curl -LSso /home/vagrant/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

# Install Python-mode
if [ ! -d "/home/vagrant/.vim/bundle/python-mode" ]; then
  git clone git://github.com/klen/python-mode.git /home/vagrant/.vim/bundle/python-mode
fi


# Enable Pathogen
echo "\" Pathogen load" > /home/vagrant/.vimrc
echo "filetype off" >> /home/vagrant/.vimrc
echo "call pathogen#infect()" >> /home/vagrant/.vimrc
echo "call pathogen#helptags()" >> /home/vagrant/.vimrc
echo "filetype plugin indent on" >> /home/vagrant/.vimrc
echo "syntax on" >> /home/vagrant/.vimrc
