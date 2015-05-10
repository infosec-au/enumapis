## EnumAPIs - Discovery of hidden API's through traversing web applications

###What?

Most web applications use Javascript in order to perform client-side logic. A very large portion of Javascript usage in web applications involves the interaction between application APIs and the front end. When pentesting web applications, such API endpoints can easily be missed or hard to find. Unless you perform every possible action that triggers such APIs, what's the chance that you'll find them, without manually going through the Javascript?

###Why?

Because I've owned shit via very obscure APIs and endpoints. This tool doesn't just do a mass regex search through Javascript files, but rather also performs intelligent enumeration. For example, a blacklist is applied for all common Javascript files (JQuery, AngularJS, KnockoutJS and more). Sometimes, there may even be endpoints in modified JQuery files.... would you have found that in a pentest?

###Usage

./enumapis.py -u https://shubh.am -o shubham_endpoints.txt -v

###Remarks

I am currently on a holiday to Tokyo, am well smashed and thought of this tool when drinking really cheap Sake from the local family mart. Much love, pentesters :)