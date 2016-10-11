To use, just install the dependency first (depends only on websocket)

    pip install -r requirements.txt

Usage of the script is simple too:

    python steempayouts.py START_BLOCK END_BLOCK X

Where as: START_BLOCK is the block we want to start scanning and END_BLOCK is where to stop. X is needed for showing top X authors/curators/posts in that blocks range.

For the above example, we run:

    python steempayouts.py 5694547 5723347 20

 So it will get the entirely statistics for 10-October-2016, showing only top 20 stats boards, sorted by VESTS or SBD.