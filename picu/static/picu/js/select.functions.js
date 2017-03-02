(function($) {
    'use strict';

    function displayFoundData(elemId, e) {
        var xyz;
        if (e.keyCode === 10 && e.keyCode === 13) {
            console.log('ignored');
        } else if (e.which != 9 && e.which != 19 && e.which != 91 && e.which != 27 && e.which != 16) {
            var val = $('#' + elemId).val();
            if(val) {
                xyz = $('#datalist_' + elemId + ' option').filter(function() {
                    return this.value === val;
                }).attr('label');
                if(xyz) {
                    $("#yay").append(xyz + "<br/>");
                    var currentVal = $("#hidden_" + elemId).val();
                    if(currentVal) $("#hidden_"+ elemId).val(currentVal + "," + val);
                }
            }
        }
        return xyz;
    }

})(django.jQuery);