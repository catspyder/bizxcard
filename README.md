## bizxcard
### introduction
a normal business card would have,
* name of the person
* position or title
* company name
* address
* phone number
* pincode
* emailId

we want to be able to fetch these data points from an image of the business card.
### challenges involved
* detecting the text from an image requires ocr
* it is not easy to predict  how much information will be in a card. some cards will just have a name and emailid while others will have a lot more
* the data included itself are of different types
* there are different ways of representing one data point a phone no can be given 12345 5645 or 123-456-7894
* as ocr is not perfect and forming fields some  data might be broken up into pieces and needs joining
* as business cards don't contain field names it is hard to know which is which
### our solution
our solution  needs to address all these problems and try to provide an optimal solution
* i created a class to hold everything fetched from the image
* then created a dictionary to identify and add these texts as key value pairs
* i stored the data in a permanent column as well as a dynamic column which removes the  data assigned to different field. if we find the name and assigned it to name field then it is removed from dynamic
* created a function to count the number of integer characters in each item in the stored list. if the no of digits is equal to 10 then we assign it as phone number. if it is 6 then we assign it as pincode
* as emails must have a particular pattern of  username@host.extension we used string matching using regex to find email ids
* then we trained a LTSM rnn model on a dataset of job titles mixed with names and place names(which are things that would be in a business card) and used this model to predict which has the highest probability of being a job title
* used the domain name of the email to try to find out the company name in the list but a better solution is being worked on
* 
