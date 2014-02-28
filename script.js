var groups = {};
var musiclist = {};

var dtype_name = ["NORMAL","HYPER","ANOTHER","NORMAL","HYPER","ANOTHER"];

function getParsedData(name, version, difficultytype, difficulty){
    var result = '<tr><td>' + version + '</td>' +
            '<td>'+ name +'</td>' +
            '<td class="gt-nowrap">' +
            '<span class="label gt-difficultylabel gt-difficultylabel-'+ dtype_name[difficultytype].toLowerCase() + ' hidden-xs">'+ dtype_name[difficultytype] + ' ' + difficulty + '</span>' +
            '<span class="label gt-difficultylabel gt-difficultylabel-small gt-difficultylabel-'+ dtype_name[difficultytype].toLowerCase() + ' visible-xs">' + difficulty + '</span></td>' +
            '<td class="gt-nowrap">' +
            '<div class="btn-group">' +
            '<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">' +
            'FULL COMBO<span class="caret"></span>' +
            '</button>' +
            '<ul class="dropdown-menu" role="menu">' +
            '<li><a href="#">FULL COMBO</a></li>' +
            '<li><a href="#">EX HARD CLEAR</a></li>' +
            '<li><a href="#">HARD CLEAR</a></li>' +
            '<li><a href="#">CLEAR</a></li>' +
            '<li><a href="#">EASY CLEAR</a></li>' +
            '<li><a href="#">ASSIST CLEAR</a></li>' +
            '<li><a href="#">FAILED</a></li>' +
            '<li><a href="#">NO PLAY</a></li>' +
            '</ul>' +
            '</div>' +
            '</td>' +
            '<td class="gt-nowrap"><input type="number" class="form-control gt-scoreinput" id="number_0000" placeholder="Score"></td></tr>'
    return result;
}

function addPanel(musicgroup){
    $('#musiclist-container').append('<div id="'+musicgroup.id+'"class="panel-heading">'+musicgroup.name+'</div>');
    $('#'+musicgroup.id).click(function(){
        if($(this).next('.panel-body')[0]){
            $(this).next('.panel-body').slideToggle();
        }else{
            $(this).after('<div class="panel-body" style="display:none"></div>');
            $(this).next('.panel-body').html('<table class="table table-striped gt-table-musiclist"><thead><tr>'+
                '<th>Ver</th>'+
                '<th>曲名</th>'+
                '<th class="gt-nowrap">難易度</th>'+
                '<th class="gt-nowrap">ランプ</th>'+
                '<th class="gt-nowrap">スコア</th>'+
                '</tr></thead><tbody class="musiclist"></tbody></table>');
            $(this).next('.panel-body').children('.musiclist').html("table");
            $(this).next('.panel-body').slideDown();
        }
    });
}

$(function(){
    $.ajax({
        url: '/get-json',
        type: 'GET',
        timeout: 10000,
        /*data: {
            id: 1,
        },*/
        dataType: 'JSON'
    })
    .done(function( data ) {
        musiclist = data;

        for(var i=1;i<=12;i++){
            groups['level'+i] = {
                id: 'level'+i,
                name: 'Level '+i,
                music: [],
            };
        }

        for (var d in musiclist) {
            if(musiclist[d].spn_level > -1) groups['level'+musiclist[d].spn_level].music.push({name:d, type:0});
            if(musiclist[d].sph_level > -1) groups['level'+musiclist[d].sph_level].music.push({name:d, type:1});
            if(musiclist[d].spa_level > -1) groups['level'+musiclist[d].spa_level].music.push({name:d, type:2});
        }

        $('#musiclist-container').html('');
        for(var i=1;i<=12;i++){
            addPanel(groups['level'+i]);
        }
        //$("#musiclist").html('');

        /*for (var d in musiclist) {
            if(musiclist[d].spn_level > -1) $("#musiclist").append(getParsedData(d, musiclist[d].version, 0, musiclist[d].spn_level));
            if(musiclist[d].sph_level > -1) $("#musiclist").append(getParsedData(d, musiclist[d].version, 1, musiclist[d].sph_level));
            if(musiclist[d].spa_level > -1) $("#musiclist").append(getParsedData(d, musiclist[d].version, 2, musiclist[d].spa_level));
        }*/
    })
    .fail(function(xhr, status, error) {
        alert(status);
    })
    .always(function( data ) {
    });
});