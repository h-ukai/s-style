( function( $ ) {
  $.fn.render = function( data ) {
    var result = new Builder( this, data ).print();
    $( this ).parent().empty().append( result );
  };

  var Builder = function() {
    this.init.apply( this, arguments );
  };
  Builder.prototype = {
    init: function( tmpl, data ) {
      this.buf = null;
      this.data = data;
      this.tmpl = $( tmpl );
      this.build();
    },
    build: function() {
      this.buf = $( '<div>' );
      for( var i = 0, len = this.data.length; i < len; i++ ) {
        var tmp = this.tmpl.clone();
        for( v in this.data[i] ) {
          var d = this.data[i][v];
          tmp.find( '.' + v ).text( d );
        }
        this.buf.append( tmp );
      }
    },
    print: function() {
      return this.buf.children();
    }
  };

} )( jQuery );