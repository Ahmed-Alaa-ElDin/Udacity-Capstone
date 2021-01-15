$(function() {
    $('#movie-actor').chosen();

    var checkToken = new AuthCheck();

    checkToken.printToken();

    // check if logged in 
    if (checkToken.load_jwts()) {
        $("#logInButton, #signUpButton").addClass('d-none');
        $("#logOutButton").removeClass('d-none');
    } else {
        $("#logInButton, #signUpButton").removeClass('d-none');
        $("#logOutButton").addClass('d-none');
    }


    // logout button
    $("#logOutButton").click(function(e) {
        e.preventDefault();
        checkToken.logout();
        checkToken.printToken();
        window.location.replace("/");
    })


    // check permissions for movies 
    // get all movies
    $("#getMovieButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('get:movies')) {
            window.location.href = '/movies';
        } else {
            alert("You don't have a premession to enter this page");
        }
    })

    // create new movie
    $("#createMovieButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('post:movie')) {
            window.location.href = '/movies/create';
        } else {
            alert("You don't have a premession to add new movie");
        }
    })

    // edit movie
    $(".editMovieButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('patch:movie')) {
            $(this).parent().submit();
        } else {
            alert("You don't have a premession to edit movies");
        }
    })

    // delete movie
    $(".deleteMovieButton").on('click', function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('delete:movie')) {
            var movie_id = $(this).data('id');
            if (confirm("Are You sure you want to delete this movie ??")) {
                $.ajax({
                    url: '/movies/delete/' + movie_id,
                    method: 'DELETE',
                    data: JSON.stringify({
                        'id': movie_id
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: function() {
                        alert("Movie deleted successfully")
                        window.location.replace("/movies");
                    }
                })
            }
        } else {
            alert("You don't have a premession to delete movies");
        }
    })

    // check permissions for actors 
    // get all actors
    $("#getActorButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('get:actors')) {
            window.location.href = '/actors';
        } else {
            alert("You don't have a premession to enter this page");
        }
    })

    // create new actor
    $("#createActorButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('post:actor')) {
            window.location.href = '/actors/create';
        } else {
            alert("You don't have a premession to add new actor");
        }
    })

    // edit actor
    $(".editActorButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('patch:actor')) {
            $(this).parent().submit();
        } else {
            alert("You don't have a premession to edit actors");
        }
    })

    // delete actor
    $(".deleteActorButton").click(function(e) {
        e.preventDefault();
        if (checkToken.checkPrem('delete:actor')) {
            var actor_id = $(this).data('id');
            if (confirm("Are You sure you want to delete this actor ??")) {
                $.ajax({
                    url: '/actors/delete/' + actor_id,
                    method: 'DELETE',
                    data: JSON.stringify({
                        'id': actor_id
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    success: function() {
                        alert("Actor deleted successfully")
                        window.location.replace("/actors");
                    }

                })
            }
        } else {
            alert("You don't have a premession to delete actors");
        }
    })



})