var BoringFriend = (function(Backbone, Marionette) {
    var App;
    App = new Marionette.Application();

    App.addRegions({
        mainContent: '#main_content'
    });

    App.on('initialize:after', function(options) {
        var access_token = window.location.hash.substring(1, window.location.hash.length).split("=")[1];
        $.ajax({
            url: '/process/'+access_token,
            type: 'GET',
            success: function(response) {
                debugger;
            },
            error: function() {
                location.reload(true);
            }
        });
    });

    return App;
})(Backbone, Marionette);