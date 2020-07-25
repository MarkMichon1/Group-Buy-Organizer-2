# Fireworks Group Buy Organizer

### Organize Group Buys Faster

**Group Buy Organizer 2** is a web application that helps manage wholesale group buys.  Remove a lot of the overhead
involved in coordinating purchases with users.  Completely rewritten to the Django web framework with many more 
features.  Running on **[https://www.pyrogroupbuys.com](https://www.pyrogroupbuys.com)**.  

**User Features**
+ **Your own private group buy events:**  The events you create are only viewable and accessible to you and people you invite.
+ **Fast and flexible group buy system:**  No more back and forth between participants and the organizer.  Want to
change your order?  Just log in and make the changes.  They will instantly change the order for the organizer.
+ **Built in explanations:**  Rather than having to go back and forth between documentations or asking questions, nearly
all pages have explanations built into them, guiding the users through the various functionality and flow of the 
application.  This can easily be toggled off or back on in the user's menu when authenticated.
+ **Night Mode:** Easily switch to a darker theme for easier night reading and lower power consumption.
+ **Streamlined case-split system:** Splitting a case with others just got a lot easier.  Pledge how many items in the 
case you'd like to order, and other users can make pledges as well.  Once all of the items in the case gets accounted
for, only then it gets locked into the order.
+ **Multiple order views:**  Three different views of event orders are available for users.  The user overview view is 
a customized list showing the cases and items you've ordered, its subtotal as well as the event total.  The event 
summary view is a concise list for the organizer of how many cases to order.  The user breakdown view steps through one
item at a time, showing all of the users who bought cases of it, as well as all of the case splits for that item.
+ **Tracking payments from attendees:** For the even
+ **Chat features:**  Talk with everyone in the group both for the event itself, and on specific item pages.
+ **Share videos of the items:**  Post videos from your favorite items, and let everyone else see them as well.  Calls Youtube API to check if they are embeddable, and if so they become embedded.
+ **Export to PDF:** All order pages include a button to export the list as a PDF to be downloaded.  Pages are stripped 
down and optimized, removing the navigation bar, forms, etc.  Only black and white is used on exported pages.

**Secondary features:**
+ **Blog Page:**  With posts only able to be made by staff site members, you have a place to release site updates for all users and guests to see.
+ **Email Functionality:** Send both activation emails and password reset emails.
+ **reCAPTCHA support:**  Built in anti-bot protection on user registration, login, and event creation forms.

**Next on roadmap:**
+ **Mobile Responsiveness:**  The app will look just as great on mobile screens as it will as a desktop app.
+ **Timezones:**  Allow the user to set their own time zone on their profile page, dynamically changing all times displayed in the templates.
+ **Added Email alerts:**  Optional email alerts for important events such as case splits opening.
+ **Tiered Pricing:**  Some wholesalers offer discounts at a certain case count, or total amount.  This will dynamically change the item pricing if these conditions are met.
+ **Brute Force Protection:** Built in measures to protect nasty bots from trying to brute force into accounts.

MIT License

Copyright (c) 2020 - ∞ Mark Michon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
