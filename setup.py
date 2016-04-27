from distutils.core import setup 
setup(name='mpinyin',
      version='0.1',
      description='a python project for getting pinyin for Chinese words or sentence',
      author='winterdawn',
      author_email='selah@outlook.com',
      url='http://www.selaselah.com',
      packages = ['mpinyin'],
      package_dir={'mpinyin':'mpinyin'},
      package_data={'mpinyin':['*.*']}
) 
