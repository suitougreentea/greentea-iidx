groups = {}
fumens = {}
dtype_name = ['NORMAL','HYPER','ANOTHER','NORMAL','HYPER','ANOTHER']
versions = ["1st style", "substream", "2nd style", "3rd style", "4th style", "5th style", "6th style", "7th style", "8th style", "9th style", "10th style", "IIDX RED", "HAPPY SKY", "DistorteD", "GOLD", "DJ TROOPERS", "EMPRESS", "SIRIUS", "Resort Anthem", "Lincle", "tricoro", "SPADA"]
versions_short = ["1st", "sub", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "RED", "HS", "DD", "GLD", "DJT", "EMP", "SIR", "RA", "Lin", "tri", "SPD"]
versions_num = ["1","s","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]
lamp = ["NO PLAY", "FAILED", "ASSIST CLEAR", "EASY CLEAR", "CLEAR", "HARD CLEAR", "EX HARD CLEAR", "FULL COMBO"]
lamp_short = ["NP", "FA", "AC", "EC", "CL", "HC", "EX", "FC"]
lamp_class = ["noplay", "failed", "assist", "easy", "clear", "hard", "exhard", "fullcombo"]
dp = false # if sp, false/if dp, true (debug)
changes = []

quickSort = (array, order, func, begin, end) ->
  i = begin
  j = end
  pivot = array[order[Math.floor((begin+end)/2)]]

  loop
    i++ while func(array[order[i]], pivot) < 0
    j-- while func(array[order[j]], pivot) > 0
    if i>=j then break

    temp = order[i]
    order[i] = order[j]
    order[j] = temp

    i++; j--

  if begin<i-1 then quickSort(array, order, func, begin, i-1)
  if end>j+1 then quickSort(array, order, func, j+1, end)

  return order

# func(a,b): if a>b +, a=b 0, a<b -
sort = (array, func) ->
  #return [0..array.length-1]
  #quicksort
  return quickSort(array, [0..array.length-1], func, 0, array.length-1)

checkUpdate = (fumen) ->
  if changes.indexOf(fumen) == -1
    changes.push fumen
    console.log(changes)

refreshLampClass = (groupid, i) ->
  fumen = groups[groupid].fumen[i]
  $("#td-#{groupid}-#{i} .gt-btn-clearlamp").html(lamp_short[fumen.lamp])
  $("#td-#{groupid}-#{i} .gt-btn-clearlamp").removeClass (index, css) ->
    return (css.match (/\bgt-btn-clearlamp-\S+/g) || []).join(' ');
  $("#td-#{groupid}-#{i} .gt-btn-clearlamp").addClass "gt-btn-clearlamp-#{lamp_class[fumen.lamp]}"

refreshEntry = (groupid, i) ->
  fumen = groups[groupid].fumen[i]
  #$("#td-#{groupid}-#{i} input[name='score']").val fumen.prevscore
  $("#td-#{groupid}-#{i} input[name='score']").val fumen.score
  #$("#td-#{groupid}-#{i} input[name='bp']").val fumen.prevbp
  $("#td-#{groupid}-#{i} input[name='bp']").val fumen.bp
  refreshLampClass(groupid, i)
  #$("#td-#{d.id}-#{d.num} .gt-btn-clearlamp").removeClass (index, css) ->
  #  return (css.match (/\bgt-btn-clearlamp-\S+/g) || []).join(' ');
  #$("#td-#{d.id}-#{d.num} .gt-btn-clearlamp").addClass "gt-btn-clearlamp-#{lamp_class[d.lamp]}"

refreshEntries = (fumen, calledgroupid) ->
  for d, i in fumen.parentgroups
    if d.id == calledgroupid then continue
    refreshEntry(d.id, d.num)

refreshFolderInfo = (groupid) ->
  lampcount = []
  for d, i in groups[groupid].fumen
    if lampcount[d.lamp] then lampcount[d.lamp]++ else lampcount[d.lamp]=1
  for i in [7..0]
    percentage = lampcount[i]/groups[groupid].fumen.length*100
    $("#panelbody-#{groupid} .gt-progress-lamp").append("""<div class="progress-bar gt-progress-bar-#{lamp_class[i]}" style="width: #{percentage}%"></div>""")

refreshVisibility = (groupid) ->
  for d, i in groups[groupid].fumen
    if groups[groupid].visibility[d.type] then $("#td-#{groupid}-#{i}").show() else $("#td-#{groupid}-#{i}").hide()

setLamp = (fumen, lamp, calledgroupid, i) ->
  fumen.lamp = lamp
  refreshLampClass(calledgroupid, i)
  refreshEntries(fumen, calledgroupid)
  checkUpdate(fumen)

addMusicEntryEdit = (groupid, i) -> #TODO: not td-version0-0, but tr-version0-0
  fumen = groups[groupid].fumen[i]
  el = $("#folder-#{groupid}").next(".panel-body").find(".musiclist").append """<tr id="td-#{groupid}-#{i}">
    <td>#{versions_num[fumen.version]}</td>
    <td>#{fumen.name}</td>
    <td class="gt-nowrap">
      <span class="label gt-difficultylabel gt-difficultylabel-#{dtype_name[fumen.type].toLowerCase()} hidden-xs">#{dtype_name[fumen.type]} #{fumen.level}</span>
      <span class="label gt-difficultylabel gt-difficultylabel-small gt-difficultylabel-#{dtype_name[fumen.type].toLowerCase()} visible-xs">#{fumen.level}</span>
    </td>
    <td class="gt-nowrap">
      <div class="btn-group">
        <button type="button" class="btn btn-default dropdown-toggle gt-btn-clearlamp gt-btn-clearlamp-fullcombo" data-toggle="dropdown"></button>
        <ul class="dropdown-menu" role="menu"></ul>
      </div>
    </td>
    <td class="gt-nowrap"><div class="form-group"><input type="text" class="form-control gt-scoreinput" name="score" placeholder="#{fumen.notes*2}"></div></td>
    <td class="gt-nowrap"><div class="form-group"><input type="text" class="form-control gt-scoreinput" name="bp" placeholder="BP"></div></td>
    </tr>"""

  refreshEntry(groupid, i)

  $("#td-#{groupid}-#{i} input[name='score']").keyup ->
    value = $(this).val()
    if !value or ($.isNumeric(value) and !value.match(/[^0-9]/) and value >= 0 and value <= fumen.notes*2)
      $(this).parent().removeClass "has-error" #.parent(".form-group")
    else
      $(this).parent().addClass "has-error"

  $("#td-#{groupid}-#{i} input[name='bp']").keyup ->
    value = $(this).val()
    if !value or ($.isNumeric(value) and !value.match(/[^0-9]/) and value >= 0)
      $(this).parent().removeClass "has-error" #.parent(".form-group")
    else
      $(this).parent().addClass "has-error"

  $("#td-#{groupid}-#{i} input[name='score']").change ->
    $(this).parent().removeClass "has-error"
    value = $(this).val()
    if !value or ($.isNumeric(value) and !value.match(/[^0-9]/) and value >= 0 and value <= fumen.notes*2)
      if !value then value = null else value = Number(value)
      fumen.score = value
      refreshEntries(fumen, groupid)
      checkUpdate(fumen)
    else
      $(this).val(fumen.score)

  $("#td-#{groupid}-#{i} input[name='bp']").change ->
    $(this).parent().removeClass "has-error"
    value = $(this).val()
    if !value or ($.isNumeric(value) and !value.match(/[^0-9]/) and value >= 0)
      if !value then value = null else value = Number(value)
      fumen.bp = value
      refreshEntries(fumen, groupid)
      checkUpdate(fumen)
    else
      $(this).val(fumen.bp)

  $("#td-#{groupid}-#{i} .gt-btn-clearlamp").click ->
    for j in [7..0]
      do (j) ->
        $("#td-#{groupid}-#{i} .dropdown-menu").append("""<li class="gt-menu-#{lamp_class[j]}"><a href="#">#{lamp[j]}</a></li>""")
        $("#td-#{groupid}-#{i} .gt-menu-#{lamp_class[j]} a").click -> setLamp(fumen, j, groupid, i); $("#td-#{groupid}-#{i} .dropdown-menu").dropdown("toggle"); return false;
        return

addMusicEntryView = (groupid, i) ->
  fumen = groups[groupid].fumen[i]
  el = $("#folder-#{groupid}").next(".panel-body").find(".musiclist").append """<tr id="td-#{groupid}-#{i}">
    <td>#{versions_num[fumen.version]}</td>
    <td>#{fumen.name}</td>
    <td class="gt-nowrap">
      <span class="label gt-difficultylabel gt-difficultylabel-#{dtype_name[fumen.type].toLowerCase()} hidden-xs">#{dtype_name[fumen.type]} #{fumen.level}</span>
      <span class="label gt-difficultylabel gt-difficultylabel-small gt-difficultylabel-#{dtype_name[fumen.type].toLowerCase()} visible-xs">#{fumen.level}</span>
    </td>
    <td class="gt-nowrap">
      <div class="btn-group">
        <button type="button" class="btn btn-default dropdown-toggle gt-btn-clearlamp gt-btn-clearlamp-fullcombo" data-toggle="dropdown"></button>
        <ul class="dropdown-menu" role="menu"></ul>
      </div>
    </td>
    <td class="gt-nowrap"><div class="form-group"><input type="text" class="form-control gt-scoreinput" name="score" placeholder="#{fumen.notes*2}"></div></td>
    <td class="gt-nowrap"><div class="form-group"><input type="text" class="form-control gt-scoreinput" name="bp" placeholder="BP"></div></td>
    </tr>"""

addPanel = (musicgroup) ->
  $('#musiclist-container').append("""<div id="folder-#{musicgroup.id}" class="panel-heading gt-folderpanel-#{musicgroup.class}">#{musicgroup.name}</div>""");
  $("""#folder-#{musicgroup.id}""").click ->
    if $(this).next(".panel-body")[0]
      $(this).next(".panel-body").slideToggle()
    else
      $(this).after("""<div id="panelbody-#{musicgroup.id}" class="panel-body" style="display:none"></div>""")
      $(this).next(".panel-body").html(
        """<div id="foldersetting-#{musicgroup.id}" class="gt-foldersetting">
        <div class="progress gt-progress-lamp"></div>
        <div class="btn-group" data-toggle="buttons">
        <button type="button" class="btn btn-default active"><input type="checkbox" name="visibility-normal">NORMAL</button>
        <button type="button" class="btn btn-default active"><input type="checkbox" name="visibility-hyper">HYPER</button>
        <button type="button" class="btn btn-default active"><input type="checkbox" name="visibility-another">ANOTHER</button>
        </div>
        </div>
        <hr>
        <table class="table table-striped gt-table-musiclist"><thead><tr>
        <th>Ver</th>
        <th>曲名</th>
        <th class="gt-nowrap">難易度</th>
        <th class="gt-nowrap">ランプ</th>
        <th class="gt-nowrap">スコア</th>
        <th class="gt-nowrap">BP</th>
        </tr></thead><tbody class="musiclist"></tbody></table>
        """)
      sortedlist = sort(
        musicgroup.fumen,
        (a, b) ->
          if a.name == b.name then return a.type - b.type
          if a.name > b.name then return 1
          if a.name < b.name then return -1
      )
      for d, i in sortedlist
        if mode=="edit" then addMusicEntryEdit(musicgroup.id, d, i)
        else if mode=="view" then addMusicEntryView(musicgroup.id, d, i)

      for i in [(if dp then 3 else 0)..(if dp then 5 else 2)]
        do (i) ->
          $("#panelbody-#{musicgroup.id} input[name='visibility-#{dtype_name[i].toLowerCase()}']").change -> musicgroup.visibility[i]=$(this).is(':checked'); refreshVisibility(musicgroup.id)
      refreshFolderInfo musicgroup.id

      $(this).next('.panel-body').slideDown()

addFumenToGroup = (groupid, fumen) ->
  groups[groupid].fumen.push fumen
  fumen.parentgroups.push {id: groupid, num: groups[groupid].fumen.length-1}

$ ->
  # fumen, group
  $.ajax '/get-json',
    type: 'GET'
    timeout: 100000
    dataType: 'JSON'
    success: (musicjson, status_1, xhr_1) ->
      #score
      $.ajax "/get-json",
        type: "GET"
        timeout: 10000
        data: {
          user: if mode=="edit" then currentUser else targetUser
        }
        dataType: "JSON"
        success: (scorejson, status_2, xhr_2) ->
          for key, value of musicjson
            for i in [(if dp then 3 else 0)..(if dp then 5 else 2)]
              if value.level[i] > 0 then fumens["#{key}-#{i}"]={name:key, type:i, version:value.version, level:value.level[i], notes:value.notes[i], parentgroups:[], lamp:0, prevlamp:0, score:null, prevscore:null, bp:null, prevbp:null}

          for i in [1..12]
            groups["level#{i}"] = {
              id: "level#{i}"
              class: "level"
              name: "Level #{i}"
              visibility: [true, true, true, true, true, true]
              fumen: []
            }

          for d, i in versions
            groups["version#{i}"] = {
              id: "version#{i}"
              class: "version"
              name: d
              visibility: [true, true, true, true, true, true]
              fumen: []
            }

          for k, d of fumens
            addFumenToGroup("version#{d.version}",d)
            addFumenToGroup("level#{d.level}",d)

          $('#musiclist-container').html ''
          for d, i in versions
            addPanel groups["version#{i}"]
          for i in [1..12]
            addPanel groups["level#{i}"]

          for k, d of scorejson
            fumens[k].prevlamp = d.lamp
            fumens[k].lamp = d.lamp
            fumens[k].prevscore = d.score
            fumens[k].score = d.score
            fumens[k].prevbp = d.bp
            fumens[k].bp = d.bp

          console.log scorejson
          console.log(fumens)
          console.log(groups)
        error: (xhr_2, status_2, error_2) ->
          alert(status)
    error: (xhr, status, error) ->
      alert(status)
    complete: (xhr, status) ->
      console.log "ajax finished"

  $("#buttonsubmit").click ->
    sendchanges = []
    for d, i in changes
      sendchanges.push {
        name: d.name
        type: d.type
        lamp: d.lamp
        score: d.score
        bp: d.bp
      }
    $.ajax "/register",
      type: "POST"
      timeout: 10000
      data: {
        changes_json: JSON.stringify(sendchanges)
      }
      dataType: "text"
      success: (data, status, xhr) ->
        console.log(data)
        changes = []
      error: (xhr, status, error) ->
        alert(status)
      complete: (xhr, status) ->
        console.log('ajax finished')

  $('#sidebar-panel').affix({
    offset: {
      top: 0
      bottom: ->
        return (this.bottom = $('footer').outerHeight(true))
    }
  })