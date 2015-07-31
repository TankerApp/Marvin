# Marvin
Marvin is a neurasthenic IRC bot for phenny (https://github.com/sbp/phenny).


## Disclaimer

Marvin is a quick and dirty python bot with many known bugs.

## Getting started

1. Copy marvin.py to your phenny/modules/ directory
2. Restart phenny

## Teach Marvin

Take Marvin in a private chat room in order to teach him.

Type : "Marvin help"

### Adding a new declaration

Marvin will randomly speak when "invoked".

Type : "Marvin ADD Today is a really sad day."

Example :

    Bob : Hey Marvin !
    Marvin : Today is a really sad day.

### Adding a new declaration with keyword

You can customize Marvin sentences bases on keywords.

Type : "Marvin ADD 42 : That number remembers me something, but what...?"

Example:

    Bob : Marvin knows something about 42
    Marvin : That number remembers me something, but what...?

### Adding a new reply

Marvin can reply to questions.

Type : "Marvin ADD? This question is totally stupid."

Example:

    Bob : Are you some king of bot Marvin ?
    Marvin : This question is totally stupid.

### Adding a new reply for a given keyword

You can customize replies depending on a keyword.

Type : "Marvin ADD? Space : I hate space and I hate you even more."

Example:

    Bob : Have you ever been into Space Marvin ?
    Marvin : I hate space and I hate you even more.


### Customizing nicks

A $nick entry will be replaced by caller's nickname.

Type : "Marvin ADD love : I love you too $nick"

Example:

    Bob : I love you Marvin
    Marvin : I love you too Bob


## Power user commands

Additional commands are available :

| Command      | Description                |
|--------------|----------------------------|
| Marvin DUMP  | List all registered quotes |
| Marvin DEL x | Drop quote number x        |


Switching to test mode:

Edit marvin.py and change PROD to 0.

You will then be able to invoke marvin using command line:

    ./marvin.py You are you Marvin ?