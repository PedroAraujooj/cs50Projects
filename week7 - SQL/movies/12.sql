SELECT movies.title FROM stars, people, movies, (SELECT movie_id AS jooj FROM people, movies, stars WHERE stars.movie_id = movies.id AND stars.person_id = people.id AND people.name = "Johnny Depp") WHERE stars.movie_id = movies.id AND stars.person_id = people.id AND stars.movie_id = jooj AND people.name = "Helena Bonham Carter";