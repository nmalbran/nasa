[NASA] Nexuiz's Anonymous Skill Appraisal
=========================================

Voting system, where `X` voters can appraise `Y` individuals on `Z` number of abilities.
The system compute the average score by individual and by ability.
The voters have a user (password only) which is hashed (to guarantee anonymity) and it's needed to vote (to guarantee one vote per voter).
The voters can change their votes and change their user.

## Origin
The system was designed to anonymously appraise the individual abilities of the local team of [Nexuiz](http://www.alientrap.org/games/nexuiz) players. However, it can be used to appraise another set of abilities in another context.

## More details
The votes are represented by a number between 0 and `MAX_VOTE_VALUE`, where 0 is "no vote" and 1 is minimum score.

## Settings
* `MAX_VOTE_VALUE`: Maximun value for voting.
* `MIN_VOTES_FOR_DISPLAY`: Minimum number of votes needed to display the results.

## Flexibility
The system accept "unlimited" and not necessarily equal number of voters, individuals and abilities. Once the voting has begun it's possible to add more voters, individuals or abilities.