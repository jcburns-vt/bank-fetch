
# Bank Fetch

## Setup

In order to use this command, you must create an account with Teller, and
create an application. You will need your application-id, as well as the
certificate.pem and private_key.pem that Teller provides for your app.

## Basic Usage

The most simplistic use case is shown below. The command shown takes your
application-id, paths to certificate.pem and private_key.pem, and the folder
that you would like to dump your bank transactions info to. Default file
format is json, you can specify csv with `--file-type csv`.

``` console
bank-fetch APPLICATION_ID OUTPUT_FOLDER --cert PATH_TO_CERTIFICATE \
    --cert-key PATH_TO_PRIVATE_KEY
```
