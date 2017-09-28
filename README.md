
# Slack AWS Lambda integration


 * Into your team slack search for `slash commands` app
 * Example of search this app link: `https://<your-team>.slack.com/apps/search?q=slash+commands`
 * Install Slach Commands and choose your own command, eg `/mycommand`
 * Go to AWS console `https://console.aws.amazon.com/lambda/home` and create a Lambda function
 * Don't use blueprints, just click into `Author from scratch` button
 * The Step 2 of Lambda creation is about triggers that will invoke our lambda, don't do nothing, just click into `Next` button
 * The Step 3 is finally about our code, into `Basic information` type your own information and choose Python 2.7
 * Still into Step 3 copy `lambda.py` form this repository and paste there type your role of your preference
 * Click into create function
 * Now we must set up one API Gateway, navigate to `https://console.aws.amazon.com/apigateway/home`
 * Click into `Create API` button, type API name and go
 * Now into Select Option called `Actions` choose create method, choose POST
 * The POST - Setup is started, choose `Lambda Function` and regtion that you created your lambda
 * Type the lambda name and move on
 * The POST - Method Execution is started, click into `Integration Request` title
 * Go to bottom of this page and Select `Body Mapping Templates`
 * Click into `Add mapping template` and type `application/x-www-form-urlencoded`
 * Insert the template code below into the text field for the template. This code converts a URL Encoded form post into JSON for your Lambda function to parse
 * Deploy API Gateway (you must create a stage)
 * Get the url and put into slack integration settings
 * Update your lambda.py now and create commands as you want

#### Template API Gateway
```
## convert HTML POST data or HTTP GET query string to JSON

## get the raw post data from the AWS built-in variable and give it a nicer name
#if ($context.httpMethod == "POST")
 #set($rawAPIData = $input.path('$'))
#elseif ($context.httpMethod == "GET")
 #set($rawAPIData = $input.params().querystring)
 #set($rawAPIData = $rawAPIData.toString())
 #set($rawAPIDataLength = $rawAPIData.length() - 1)
 #set($rawAPIData = $rawAPIData.substring(1, $rawAPIDataLength))
 #set($rawAPIData = $rawAPIData.replace(", ", "&"))
#else
 #set($rawAPIData = "")
#end

## first we get the number of "&" in the string, this tells us if there is more than one key value pair
#set($countAmpersands = $rawAPIData.length() - $rawAPIData.replace("&", "").length())

## if there are no "&" at all then we have only one key value pair.
## we append an ampersand to the string so that we can tokenise it the same way as multiple kv pairs.
## the "empty" kv pair to the right of the ampersand will be ignored anyway.
#if ($countAmpersands == 0)
 #set($rawPostData = $rawAPIData + "&")
#end

## now we tokenise using the ampersand(s)
#set($tokenisedAmpersand = $rawAPIData.split("&"))

## we set up a variable to hold the valid key value pairs
#set($tokenisedEquals = [])

## now we set up a loop to find the valid key value pairs, which must contain only one "="
#foreach( $kvPair in $tokenisedAmpersand )
 #set($countEquals = $kvPair.length() - $kvPair.replace("=", "").length())
 #if ($countEquals == 1)
  #set($kvTokenised = $kvPair.split("="))
  #if ($kvTokenised[0].length() > 0)
   ## we found a valid key value pair. add it to the list.
   #set($devNull = $tokenisedEquals.add($kvPair))
  #end
 #end
#end

## next we set up our loop inside the output structure "{" and "}"
{
#foreach( $kvPair in $tokenisedEquals )
  ## finally we output the JSON for this pair and append a comma if this isn't the last pair
  #set($kvTokenised = $kvPair.split("="))
 "$util.urlDecode($kvTokenised[0])" : #if($kvTokenised[1].length() > 0)"$util.urlDecode($kvTokenised[1])"#{else}""#end#if( $foreach.hasNext ),#end
#end
}
```