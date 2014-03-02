debug_flag = 1;
// load jQuery
(function () {
  var script = document.createElement("script");
  script.setAttribute("src", "//code.jquery.com/jquery-2.0.0.min.js");
  document.body.appendChild(script);
})();


function get_music_database(version){
  var html = document;
  if(window.location != 'http://iidxsd.sift-swift.net/view/ac/'+version+'/all'){
    window.location = 'http://iidxsd.sift-swift.net/view/ac/'+version+'/all'
  }
  try{
    get_music_size(html);
  }
  catch(e){
    if(window.location == 'http://iidxsd.sift-swift.net/view/ac/'+version+'/all'){
     window.location.reload();
    }
  }

  var music_db = {}
  meta = {} // global
  create_meta_level_index(meta)

  var versions = $(html).find('tbody.data_title');
  versions.each(function(){
    var version = this.textContent;
    var data_table = $(this).next();
    var musics = data_table.find('tr');

    meta[version] = {}
    meta[version]["music_count"] = 0
    meta[version]["index"] = []

    musics.each(function(){
      var tds = $(this).find('td');
      // each music
      var music = {}

      // Name(key)
      var name = tds[0].textContent.substr(1)
      meta[version]["music_count"] += 1
      meta[version]["index"][ meta[version]["index"].length ] = name

      music[name] = {}
      music[name].name = name
      // music[name].clear_rate // get from other site
      music[name].version = version
      // Genre
      music[name].genre = $(tds).filter('.genre').text()
      // Artist
      music[name].artist = $(tds).filter('.artist').text()
      // BPM
      var bpm_tmp = $(tds).filter('.bpm').text()
      var re = bpm_tmp.match(/(\d+)-(\d+)/)
      music[name].bpm_change = re != null
      music[name].bpm_low = music[name].bpm_change? re[1]: bpm_tmp
      music[name].bpm_high = music[name].bpm_change? re[2]: bpm_tmp
      // sp_level
      music[name].spn_level = $(tds).filter('.difn7').text()
      music[name].sph_level = $(tds).filter('.difh7').text()
      music[name].spa_level = $(tds).filter('.difa7').text()
      // sp_notes
      music[name].spn_notes = $(tds).filter('.notesn7').text()
      music[name].sph_notes = $(tds).filter('.notesh7').text()
      music[name].spa_notes = $(tds).filter('.notesa7').text()
      // dp_level
      music[name].dpn_level = $(tds).filter('.difn14').text()
      music[name].dph_level = $(tds).filter('.difh14').text()
      music[name].dpa_level = $(tds).filter('.difa14').text()
      // dp_notes
      music[name].dpn_notes = $(tds).filter('.notesn14').text()
      music[name].dph_notes = $(tds).filter('.notesh14').text()
      music[name].dpa_notes = $(tds).filter('.notesa14').text()

      // add to level index
      meta["sp_level" + music[name].spn_level + "_normal"][ meta["sp_level" + music[name].spn_level + "_normal"].length ] = name
      meta["sp_level" + music[name].sph_level + "_hyper"][ meta["sp_level" + music[name].sph_level + "_hyper"].length ] = name
      meta["sp_level" + music[name].spa_level + "_another"][ meta["sp_level" + music[name].spa_level + "_another"].length ] = name
      meta["dp_level" + music[name].dpn_level + "_normal"][ meta["dp_level" + music[name].dpn_level + "_normal"].length ] = name
      meta["dp_level" + music[name].dph_level + "_hyper"][ meta["dp_level" + music[name].dph_level + "_hyper"].length ] = name
      meta["dp_level" + music[name].dpa_level + "_another"][ meta["dp_level" + music[name].dpa_level + "_another"].length ] = name

      for(var key in music){
        music_db[key] = music[key];
      }
    })
  })

  console.log('Complete getting ' + get_hash_length(music_db) + ' musics information from ' + get_music_size(html) + ' database')
  return music_db;

}

function get_music_size(html){
  txt = $(html).find('span.msc_num').text()
  return /\D*(\d+)music/.exec(txt)[1]
}

function get_hash_length(hash){
  var len=0;
  for(var key in hash){
    len++;
  }
  return len;
}

function create_meta_level_index(meta){
  // for error
  meta["sp_level-_normal"] = []
  meta["sp_level-_hyper"] = []
  meta["sp_level-_another"] = []
  meta["dp_level-_normal"] = []
  meta["dp_level-_hyper"] = []
  meta["dp_level-_another"] = []
  // level0
  meta["sp_level0_normal"] = []
  meta["sp_level0_hyper"] = []
  meta["sp_level0_another"] = []
  meta["dp_level0_normal"] = []
  meta["dp_level0_hyper"] = []
  meta["dp_level0_another"] = []
  // level1
  meta["sp_level1_normal"] = []
  meta["sp_level1_hyper"] = []
  meta["sp_level1_another"] = []
  meta["dp_level1_normal"] = []
  meta["dp_level1_hyper"] = []
  meta["dp_level1_another"] = []
  // level2
  meta["sp_level2_normal"] = []
  meta["sp_level2_hyper"] = []
  meta["sp_level2_another"] = []
  meta["dp_level2_normal"] = []
  meta["dp_level2_hyper"] = []
  meta["dp_level2_another"] = []
  // level3
  meta["sp_level3_normal"] = []
  meta["sp_level3_hyper"] = []
  meta["sp_level3_another"] = []
  meta["dp_level3_normal"] = []
  meta["dp_level3_hyper"] = []
  meta["dp_level3_another"] = []
  // level4
  meta["sp_level4_normal"] = []
  meta["sp_level4_hyper"] = []
  meta["sp_level4_another"] = []
  meta["dp_level4_normal"] = []
  meta["dp_level4_hyper"] = []
  meta["dp_level4_another"] = []
  // level5
  meta["sp_level5_normal"] = []
  meta["sp_level5_hyper"] = []
  meta["sp_level5_another"] = []
  meta["dp_level5_normal"] = []
  meta["dp_level5_hyper"] = []
  meta["dp_level5_another"] = []
  // level6
  meta["sp_level6_normal"] = []
  meta["sp_level6_hyper"] = []
  meta["sp_level6_another"] = []
  meta["dp_level6_normal"] = []
  meta["dp_level6_hyper"] = []
  meta["dp_level6_another"] = []
  // level7
  meta["sp_level7_normal"] = []
  meta["sp_level7_hyper"] = []
  meta["sp_level7_another"] = []
  meta["dp_level7_normal"] = []
  meta["dp_level7_hyper"] = []
  meta["dp_level7_another"] = []
  // level8
  meta["sp_level8_normal"] = []
  meta["sp_level8_hyper"] = []
  meta["sp_level8_another"] = []
  meta["dp_level8_normal"] = []
  meta["dp_level8_hyper"] = []
  meta["dp_level8_another"] = []
  // level9
  meta["sp_level9_normal"] = []
  meta["sp_level9_hyper"] = []
  meta["sp_level9_another"] = []
  meta["dp_level9_normal"] = []
  meta["dp_level9_hyper"] = []
  meta["dp_level9_another"] = []
  // level10
  meta["sp_level10_normal"] = []
  meta["sp_level10_hyper"] = []
  meta["sp_level10_another"] = []
  meta["dp_level10_normal"] = []
  meta["dp_level10_hyper"] = []
  meta["dp_level10_another"] = []
  // level11
  meta["sp_level11_normal"] = []
  meta["sp_level11_hyper"] = []
  meta["sp_level11_another"] = []
  meta["dp_level11_normal"] = []
  meta["dp_level11_hyper"] = []
  meta["dp_level11_another"] = []
  // level12
  meta["sp_level12_normal"] = []
  meta["sp_level12_hyper"] = []
  meta["sp_level12_another"] = []
  meta["dp_level12_normal"] = []
  meta["dp_level12_hyper"] = []
  meta["dp_level12_another"] = []
}

$(function(){
  music_db = get_music_database(21);
  music_json = JSON.stringify(music_db);
  meta_json = JSON.stringify(meta);
  // $('body').text(JSON.stringify(music_db));
  $('body').html('\
    <form action="http://localhost:8080/add" method="post">\
        <textarea class="form-control" name=music_json id=music_json rows=10>'+music_json+'</textarea>\
        <textarea class="form-control" name=meta_json id=meta_json rows=10>'+meta_json+'</textarea>\
        <input class="form-control" type=hidden name=state id=state value="confirm">\
        <button type="submit" class="btn btn-primary" id=submit>Confirm</button>\
    </form>\
   ')
})

