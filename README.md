
# Bank Fetch

This terminal application is intended to make it simple to download your own
bank transactions in json or csv format to make use of them in a budget app or
excel sheet. You could call the bank-fetch command from a VBA macro in order to
automate the updating of your bank data.

## Setup

In order to use this command, you must create an account with Teller, and
create an application. You will need your application-id, as well as the
certificate.pem and private_key.pem that Teller provides for your app.

You must also have python and pipx installed for these instructions.

## Installation

Navigate to the root directory of this repository and run the following:

``` console
$ pipx install .
$ pipx ensurepath
```
Then restart the shell for the command to become available

## Basic Usage

The most simplistic use case is shown below. The command shown takes your
application-id, paths to certificate.pem and private_key.pem, and the folder
that you would like to dump your bank transactions info to. Default file
format is json, you can specify csv with `--file-type csv`.

``` console
$ bf APPLICATION_ID OUTPUT_FOLDER --cert PATH_TO_CERTIFICATE \
    --cert-key PATH_TO_PRIVATE_KEY
```

The first time this command is called, a browser window will be opened that
will prompt you to connect your bank account via the secure TellerConnect
widget. Subsequent calls will not require you to enter your info, so if you
want to change the associated bank, use the `--reset' flag.

Once bank data is downloaded to your device, it is your own responsibility to
ensure that it stays secured. This application is read-only and does not
have the ability to move funds.
