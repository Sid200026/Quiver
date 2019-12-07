# Guide to common tasks

Clone the repository to create a local copy
` git clone https://github.com/Sid200026/Quiver.git `   

## Making any change to the repository

#### Setup and activate a python virtual environment
`virtualenv -p python3 venv`

`source venv/bin/activate`

#### Install dependencies

##### If you have both pip and pip3 installed, then use pip3

`pip3 install -r requirements-dev.txt`

## Never ever push your changes directly to master. Always create a new branch


`source venv/bin/activate`

`git checkout -b *branchname*`

#### Now make any changes you want in your local. After that now add the file you want for staging.

#### To get the files that needs to be staged

`git status`

#### Now for each file, add them individually.
## Do not use `git add .`

`git add *filename or foldername* `
  
#### Now commit the file and have a meaningful commit description

`git commit -m "*commit description*"`

#### Now push your code to the repository. If you have created a new branch and need to push it for the first time then

` git push -u origin * branchname*` 
   
#### If you have already made pushed to the same branch before no need of -u argument
