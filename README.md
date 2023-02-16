# WebTV/MSN TV ROMFS Library

A Python library written by Eric MacDonald (eMac) that provides functions to unpack and pack files in the ROMFS filesystem used by WebTV and MSN TV. This repository contains two versions of the library, both originally written in 2021. While both have been uploaded online already, they are now being released on GitHub to make the code more accessible to those interested in using it.

Formats supported by the ROMFS library:
- Any WebTV and first-generation MSN TV app and boot ROMs (.o binary)
- Echostar DishPlayer firmware (.o binary)
- WebTV Viewer 1.0 (Flash Store & ROM Store)
- WebTV Viewer 2.5+ scrambled (Flash.vwr & ROM.vwr)
- WebTV Dreamcast (WEBTV.ROM, little-endian)

UltimateTV and MSN TV 2 firmware are not compatible with this tool as they don't use ROMFS at all - they use a completely different filesystem to store files named **CompressFS**. There are tools already available to extract files from those formats: https://archive.org/details/compressfs-tools

This library will work on Python 3.x, and is known to work with the latest Python version as of writing (3.11).

I take no credit for writing anything except the sample scripts for the old version of the ROMFS library. Big thanks goes to eMac for everything he's done to take WebTV hacking further and make it more accessible for everyone.

## Versions

- "romfs-dumper-10092021"

This is the last version of the ROMFS dumper library released to the public, last modified on September 10, 2021. Contains under the hood improvements as well as the ability to pack ROMFS data directly back into WebTV/MSN TV firmware and extract "AutoDisk" data from applicable WebTV/MSN TV builds. Comes with a sample script written by eMac to give an idea of how the library works.

- "OLD-romfs_lib_w_samples"

Older version of the ROMFS library last modified some time in early 2021. This was the first version of the ROMFS library that was able to be released to the public and is being kept in this repository for posterity's sake. Contains two sample scripts written by me (back when I was exclusively hosting this stuff on a "content archive" on the [WebTV Wiki](https://wiki.webtv.zone) for some reason) that intended to make it easier for both programmers and people simply wanting to use the tool to understand how it worked.

## How to Use

Simply take the ROMFS library you want to use ("romfs-dumper-10092021" is recommended), and import any code you want to use from it in your scripts from the lib folder. Reading the sample scripts will give you more insight on what you can do with this library.