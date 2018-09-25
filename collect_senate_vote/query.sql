SELECT Count(*), senator.party
FROM senator INNER JOIN vote ON senator.sname = vote.sname
where vote.vote = 'Nay'
group by senator.party
