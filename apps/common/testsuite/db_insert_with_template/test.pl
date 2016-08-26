

my $now = DateTime->now;
my $date = DateTime->now->date;
my $name = Sys::Hostname::hostname;
my $col_name = "test-".$name."-".$now;

my $t = db_get_template("LatticePolytopes", "SmoothReflexive", template_key=>"fano");
db_set_type_info("Test", $col_name, template=>$t->{template}, template_key=>$col_name, app=>"polytope", basic_type=>"polytope::Polytope<Rational>", id=>$col_name);
my $s = db_get_template("Test", $col_name, template_key=>$col_name);

my $parray = load_data("1_in.pdata");
db_insert_array($parray, "Test", $col_name, use_template=>1, template_key=>$col_name);

my $count = db_count({}, db=>"Test", collection=>$col_name);

my $retarray = db_query({}, db=>"Test", collection=>$col_name, sort_by=>{"_id"=>1});

foreach (@{db_ids({}, db=>"Test", collection=>$col_name)}) {
	db_remove($_, "Test", $col_name);
}

compare_values( 'count', 18, $count );
compare_data('1',$retarray);
compare_values( 'remove', 0, db_count({}, db => "Test", collection => $col_name) );
db_clean_up_test();
