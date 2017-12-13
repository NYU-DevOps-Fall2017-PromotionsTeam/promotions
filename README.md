# promotions
[![Build Status](https://travis-ci.org/NYU-DevOps-Fall2017-PromotionsTeam/promotions.svg?branch=master)](https://travis-ci.org/NYU-DevOps-Fall2017-PromotionsTeam/promotions)
[![Codecov](https://img.shields.io/codecov/c/github/NYU-DevOps-Fall2017-PromotionsTeam/promotions.svg)](https://codecov.io/gh/NYU-DevOps-Fall2017-PromotionsTeam/promotions)  
RESTful API for information pertaining to Sales (e.g., buy 2 get 1 free, 20% off)

## Production Server  
http://nyu-promotion-service-f17-prod.mybluemix.net/
 
### Api Docs  
http://nyu-promotion-service-f17-prod.mybluemix.net/promotions/api

## Development Server  
http://nyu-promotion-service-f17.mybluemix.net/

### Try it out  
REST API Calls -> @ url http://nyu-promotion-service-f17-prod.mybluemix.net/promotions

We recommend using this REST Client:  
https://install.advancedrestclient.com/#/install

## Setup 
1. Clone and cd into the Repo  
```
git clone https://github.com/NYU-DevOps-Fall2017-PromotionsTeam/promotions
```
2. Boot the VM  
```
vagrant up && vagrant ssh
```
3. cd into shared /vagrant file
```
cd /vagrant
```

### Run Tests Before Doing Anything
```
nosetests &&
python3 run.py &
behave
```
Make sure the Server is running by going to http://localhost:5001/

### Kill The Server If You Want
You should probably do this before contributing to the project
```
kill $(ps aux | grep 'python3 run.py' | grep -v grep | awk '{print $2}')
```

### Alternatively
This script will run tests and clean-up the running server when done
```
./run_tests.sh
```

## Authors

* **Joe Zuhusky** - jzuhusky@nyu.edu
* **Da Ying** - dy877@nyu.edu
* **Diqing Zhu** - dz1120@nyu.edu
* **Jincong Zhu** - jz2668@nyu.edu

