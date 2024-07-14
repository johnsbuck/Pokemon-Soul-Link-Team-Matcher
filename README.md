# Pokémon Soul Link Matcher

## Introduction
After watching some Pokémon Soul Link videos and streams with Ray Narvaez Jr (https://www.youtube.com/brownman & https://www.twitch.tv/ray) and Shen (https://www.twitch.tv/shenpai & https://www.youtube.com/AeroViro), I wanted to make a program that could solve a problem of theirs, that is trying to figure out what Pokémon they could use to make the best team. While I don't know how to quantify "best" Pokémon team, I did create a program that could generate all unique Pokémon teams that would have some value for.

## What is a Soul Link
A Pokémon Soul Link (or Soul Link Nuzlocke) is a challenge where two players who are playing the same Pokémon game have to impose the following rules on themselves:

1. Any Pokémon that faints must be released or boxed permanently. It is considered “dead” for the rest of the challenge.
2. Only the first wild Pokémon encountered in a route or area can be caught. If the player fails to catch it (ie. it flees or faints), their opportunity to catch a Pokémon in that area is lost.
3. The player must nickname all Pokémon they catch or obtain. (This is not technically necessary for the challenge run, but is universally accepted as part of a Nuzlocke.)

On top this, they have to impose the following rules on each other:

4. The two players play through the same game (or different games in the same generation, such as X and Y) simultaneously.
5. Encounters for players on each route are linked. If one player fails to catch their encounter for a route, the other player must box or release their encounter for that route as well. If both players successfully catch their first encounter for the route, those two Pokémon are “linked” as partners.
6. When one player’s Pokémon faints, its partner on the other player’s team must be boxed or released as well.
7. If a Pokémon is placed in the PC, its partner on the other player’s team must be placed in the PC as well.

If these rules do not sound difficult enough, Ray and Shen decided to add two more rules into the mix:

8. Often, players will restrict the use of shared types between the teams, meaning that no Pokémon on either team may share the same primary type.
9. It’s common to randomize the encounters on each route for this challenge, to promote greater Pokémon and type variety between the teams, especially on early routes where Pokémon selection is limited.

For more info, refer to https://nuzlockeuniversity.ca/nuzlocke-variants/soul-link-nuzlocke-rules/.

## How does this script help?
Goes through a list of Pokemon caught by both players. This list is a CSV file in the following format:


* Player 1's Pokémon Name
* Player 1's Pokémon Type
* Player 2's Pokémon Name
* Player 2's Pokémon Type

**Example**
```csv
Blaziken,Fire,Claydol,Ground
```

The script pulls all this info and formats it into a list of Pokémon pairs. From this list of pairs, it goes through all possible options to find every team of Pokémon (1 to 6 per team) that has all unique types within both player's teams. On top of this, we check to ensure that we do not list an existing sub-team, such as listing a Pokémon team of 2 when both are already together in a team of 3 or 4.

## Does it work on more than 2 players?
No.

## Will you add that capability?
Who would want to play an n-player Pokémon Soul Link? They can torture themselves.