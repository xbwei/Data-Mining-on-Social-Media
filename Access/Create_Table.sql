
CREATE TABLE  tweet
(
  
  TweetID Text,
   TweetText Text,
   
   UserID  Text,
   
   TweetTime  Text,
   
 PRIMARY KEY(TweetID)
 
);

CREATE TABLE  user
(
  
  UserID  Text,
   
 UserName  Text,
 
PRIMARY KEY(UserID)

);


ALTER TABLE tweet
   
 ADD    FOREIGN KEY (UserID)
  
  REFERENCES user(UserID);
  
