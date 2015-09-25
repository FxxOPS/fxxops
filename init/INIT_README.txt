# build environment

## install git
yum install git -y

## sign in
https://github.com/
join ops team


## get github branch: dev
cd  /<ur_home_dir>/dev
git clone -b dev https://github.com/FxxOPS/fxxops.git


## ignore useless file
cd fxxops
vi .gitignore
.idea
.gitignore
*.pyc


## change config.ini
cd fxxops
[LOGGER]
Level=DEBUG
Path=/tmp/host_list.log


## create own database 
mysql -uroot -p123456 -h10.1.110.24
CREATE DATABASE <ur_db_name>  DEFAULT CHARACTER SET utf8;
mysql -uroot -p123456 <ur_db_name>  < <ur_initsql_dir>/init.sql

## change connect db way (notice: make sure it !!)
vi Database/const.py
DB_ADDRESS = '10.1.110.24'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = '123456'
DB_CHAR_SET = 'utf8'
DB_DEF = '<ur_db_name>'


## change port to another port
vi run.py
e.g:
WebApp.run("0.0.0.0", 8002, True)

## skip privilege

vi LoginViews.py
# inputPass = hashlib.md5(hashlib.md5("%s-%s" % (form.strPassword.data, strCtime)).hexdigest()).hexdigest().upper()
inputPass = 'B96D4F26CF3B6B9FCC732941BB283460'



## view web
python  run.py
http://10.1.110.25:8002/
admin/1234



# before code (how can use git, u can see git_cmd.txt)

## create ur local branch (local branch is used develop, fix bug, test)
git branch (check ur branch)
git branch <local_branch_name> (e.g: git brach dev-domain)

## merge main dev branch (when u finish ur develop , fix bug and test ,make sure that it is right ,then use it)
## change ur local branch
git checkout dev-domain
git commint -m "<comment>"


## change ur main dev branch and merge
git checkout dev
git merge dev-domain