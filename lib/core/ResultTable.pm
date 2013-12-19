package core::resulttable;

use MooseX::Declare;

# Base class for all tasks
class ResultTable {
    use XML::Writer;

    use constant {
        TAG_MAIN => "gtta-table",
        TAG_ROW => "row",
        TAG_CELL => "cell",
        TAG_COLUMNS => "columns",
        TAG_COLUMN => "column",
        ATTR_NAME => "name",
        ATTR_WIDTH => "width"
    };

    has "columns" => (is => "rw", required => 1);
    has "rows" => (is => "rw", default => sub {[]});

    # Add row to table
    method add_row($row) {
        push @{$self->rows}, $row;
    }

    # Render a table
    method render {
        my ($output, $xml);

        $output = "";
        $xml = XML::Writer->new(OUTPUT => \$output);

        $xml->startTag($self->TAG_MAIN);
        $xml->startTag($self->TAG_COLUMNS);

        foreach my $column (@{$self->columns}) {
            $xml->startTag($self->TAG_COLUMN, name => $column->{"name"}, width => $column->{"width"});
            $xml->endTag();
        }

        $xml->endTag();

        foreach my $row (@{$self->rows}) {
            $xml->startTag($self->TAG_ROW);

            foreach my $cell (@$row) {
                $xml->dataElement($self->TAG_CELL, $cell);
            }

            $xml->endTag();
        }

        $xml->endTag();

        return $output;
    }
}
