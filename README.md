
# Slack AWS Lambda integration

[![Build Status](https://travis-ci.org/pvgomes/slack-lambda.svg?branch=master)](https://travis-ci.org/pvgomes/slack-lambda)

### Steps to configure your integration
 * First of all, generate .zip file from this code that we'll deploy `zip -r ../slack-lambda.zip ./`
 * Inside your slack team search for `slash commands` app
 * Example of search this app link: `https://<your-team>.slack.com/apps/search?q=slash+commands`
 * Install Slack Commands and choose your own command, eg `/mycommand`
 * Go to AWS console `https://console.aws.amazon.com/lambda/home` and create a Lambda function
 * Don't use blueprints, just click on `Author from scratch` button
 * Into `Basic information` type your own information and click Create function
 * Into Configuration select Python 3.6 as Runtime, choose `Upload a .ZIP file` and into Handle type main.lambda_handler which will call our entry function and finally upload our slack-lambda.zip
 * Save and test our lambda, configure this simple body as test: `{"text": "help"}`
 * Now we must set up one API Gateway, navigate to `https://console.aws.amazon.com/apigateway/home`
 * Click into `Create API` button, type API name and go
 * Now into Select Option called `Actions` choose create method, choose POST
 * The POST - Setup is started, choose `Lambda Function` and region that you created your lambda
 * Type the lambda name and move on
 * The POST - Method Execution is started, click into `Integration Request` title
 * Go to bottom of this page and Select `Body Mapping Templates`
 * Click into `Add mapping template` and type `application/x-www-form-urlencoded`
 * Insert the template code below into the text field for the template. This code converts a data Encoded form post into JSON for your Lambda function to parse, save it.
 * Into Actions, deploy API Gateway (you must create a stage)
 * Get the url and put into slack integration settings

Now you have a structure to execute commands from Slack and you can do everything that you want.

Enjoy


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