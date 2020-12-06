# Auction House
Final project for SDA course.

# Description
Available features:
* User creation and management
* Auction creation, bidding, purchase (aka BuyNow)
* Auction list view, search, filter by category and sort
* Ability to view own auctions, bids and purchases


# Technologies Used
Project is built using the following:
* Python 3.8
* Django 3.1
* MySQL 8.0
* Bootstrap 4


# Installation
What you will need to run it:
> python 3.8

> pip install django

> MySQL DB

> venv (optional)

NOTE: update settings.py to reflect your MySQL DB settings or create them likewise

Once the above are done:
> python manage.py makemigrations

> python manage.py migrate

and lastly
> python manage.py runserver

# Final word
This project is not complete, yet functional to the extent of above-mentioned features. What was planned, but not finished:
* Refreshing auctions to reflect their status (active vs inactive)
* Seller and buyer ratings
* Transaction overview
* Balance on users account
* Implementation of Promoted auctions (to have them listed first for every search)
* Auction conclusion with email notification
