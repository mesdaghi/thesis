#!usr/bin/perl

use strict;
use warnings;

#my $file = $ARGV[0];
my $seq_file = $ARGV[0];
my $res_1 = $ARGV[1]; $res_1 --;
my $res_2 = $ARGV[2]; $res_2 --;

my $seq = <>;
$seq  = <>;

my @list = split //, $seq;
my @new_list = @list[$res_1..$res_2];
my $new_seq = join '',@new_list;
print $new_seq,"\n"; 


