/**
 * Created by zxl on 16-6-1.
 */
$(document).ready(function() {
      $('#info-change-form').on('submit', function(e) {
          alert('进入到这里来了');
          return false;
      });

});
function info_change(user_id){
    alert('userId: '+user_id);
    $('#info-change-form').submit()
}