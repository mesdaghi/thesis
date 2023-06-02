use strict;
use warnings 'all';

my (%fasta, @keys);

{
    my $key;

    while ( <> ) {

        chomp;

        if ( s/^>\K/REV/ ) {
            $key = $_;
            push @keys, $key;
        }
        elsif ( $key ) {
            unshift @{ $fasta{$key} }, scalar reverse;
        }
    }
}

for my $key ( @keys ) {
    print $key, "\n";
    print "$_\n" for @{ $fasta{$key} };
}
