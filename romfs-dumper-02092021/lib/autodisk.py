import os.path
import binascii
import struct
from lib.build_meta import *


"""
    Bytes 0-4: Autodisk File Database Index/Metadata Magic [0x39592841]
    Bytes 4-8: Index/Metadata Checksum
    Bytes 8-12: ??? version?
    Bytes 12-16: ??? version?
    Bytes 16-20: Size in bytes of the file DB index/metadata section needs to be smaller than 0x10001
    Bytes 20-24: Number of files in the DB needs to be smaller than 0x401
    Bytes 24-XXX: File Index/Metadata
        DWORD[0]: ??? version?
        DWORD[1]: file size
        DWORD[2]: file data offset
        DWORD[3]: file name offset
        DWORD[4]: crc32 of file data

    Bytes XXX:XXX+4 File Data Magic [0x11993456]
    Bytes XXX+4:ZZZ: File Data
"""
class autodisk():
    """
    ROM:805DCC14 GetHeader:                               # CODE XREF: AutoDisk__ExtractFilesRead:loc_805DC930↑p
    ROM:805DCC14                 lw      $v0, 0x80003234
    ROM:805DCC1C                 addiu   $sp, -0x28
    ROM:805DCC20                 sw      $ra, 0x20($sp)
    ROM:805DCC24                 sw      $s3, 0x1C($sp)
    ROM:805DCC28                 sw      $s2, 0x18($sp)
    ROM:805DCC2C                 sw      $s1, 0x14($sp)
    ROM:805DCC30                 beqz    $v0, loc_805DCD64
    ROM:805DCC34                 sw      $s0, 0x10($sp)
    ROM:805DCC38                 beqz    $v0, loc_805DCC48
    ROM:805DCC3C                 lui     $v0, 0x8001
    ROM:805DCC40                 j       loc_805DCC4C
    ROM:805DCC44                 lw      $s0, 0x80016B50
    ROM:805DCC48  # ---------------------------------------------------------------------------
    ROM:805DCC48
    ROM:805DCC48 loc_805DCC48:                            # CODE XREF: GetHeader+24↑j
    ROM:805DCC48                 move    $s0, $zero
    ROM:805DCC4C
    ROM:805DCC4C loc_805DCC4C:                            # CODE XREF: GetHeader+2C↑j
    ROM:805DCC4C                 lw      $v0, 0x10($s0)
    ROM:805DCC50                 move    $a0, $s0
    ROM:805DCC54                 lw      $v0, 0x3C($v0)
    ROM:805DCC58                 jalr    $v0
    ROM:805DCC5C                 move    $a1, $zero
    ROM:805DCC60                 move    $a0, $v0
    ROM:805DCC64                 move    $a1, $zero
    ROM:805DCC68                 jal     AllocateMemory_Dup2
    ROM:805DCC6C                 move    $a2, $zero
    ROM:805DCC70                 jal     MaxiBrowserSize
    ROM:805DCC74                 move    $s1, $v0
    ROM:805DCC78                 move    $a0, $s0
    ROM:805DCC7C                 lw      $v1, 0x10($s0)
    ROM:805DCC80                 move    $a1, $zero
    ROM:805DCC84                 lw      $v1, 0x3C($v1)
    ROM:805DCC88                 jalr    $v1
    ROM:805DCC8C                 move    $s0, $v0
    ROM:805DCC90                 move    $a0, $s1
    ROM:805DCC94                 move    $a1, $s0
    ROM:805DCC98                 jal     ReadBrowserStorage_Dup2
    ROM:805DCC9C                 move    $a2, $v0
    ROM:805DCCA0                 bnez    $v0, loc_805DCD5C
    ROM:805DCCA4                 move    $a0, $s1
    ROM:805DCCA8                 lui     $v0, 0x3959
    ROM:805DCCAC                 lw      $v1, 0($s1)
    ROM:805DCCB0                 li      $v0, 0x39592841
    ROM:805DCCB4                 bne     $v1, $v0, loc_805DCD5C
    ROM:805DCCB8                 li      $v0, 1
    ROM:805DCCBC                 lw      $v1, 8($s1)
    ROM:805DCCC0                 bne     $v1, $v0, loc_805DCD5C
    ROM:805DCCC4                 lui     $v0, 1
    ROM:805DCCC8                 lw      $s2, 0x10($s1)
    ROM:805DCCCC                 lw      $s3, 4($s1)
    ROM:805DCCD0                 slt     $v0, $s2
    ROM:805DCCD4                 bnez    $v0, loc_805DCD5C
    ROM:805DCCD8                 lw      $v1, 0x14($s1)
    ROM:805DCCDC                 slti    $v0, $v1, 0x401
    ROM:805DCCE0                 beqz    $v0, loc_805DCD5C
    ROM:805DCCE4                 nop
    ROM:805DCCE8                 jal     AllocateMemorySystemNilAllowed_Dup2
    ROM:805DCCEC                 move    $a0, $s2
    ROM:805DCCF0                 move    $s0, $v0
    ROM:805DCCF4                 beqz    $s0, loc_805DCD5C
    ROM:805DCCF8                 move    $a0, $s1
    ROM:805DCCFC                 jal     MaxiBrowserSize
    ROM:805DCD00                 nop
    ROM:805DCD04                 move    $a0, $s0
    ROM:805DCD08                 move    $a1, $v0
    ROM:805DCD0C                 jal     ReadBrowserStorage_Dup2
    ROM:805DCD10                 move    $a2, $s2
    ROM:805DCD14                 bnez    $v0, loc_805DCD50
    ROM:805DCD18                 lui     $v0, 0x1199
    ROM:805DCD1C                 addu    $v1, $s0, $s2
    ROM:805DCD20                 lw      $v1, -4($v1)
    ROM:805DCD24                 li      $v0, 0x11993456
    ROM:805DCD28                 bne     $v1, $v0, loc_805DCD50
    ROM:805DCD2C                 nop
    ROM:805DCD30                 jal     InitCrc32_Dup2
    ROM:805DCD34                 nop
    ROM:805DCD38                 move    $a0, $v0
    ROM:805DCD3C                 addiu   $a1, $s0, 8
    ROM:805DCD40                 jal     UpdateCrc32_Dup2
    ROM:805DCD44                 addiu   $a2, $s2, -8
    ROM:805DCD48                 beq     $v0, $s3, loc_805DCD68
    ROM:805DCD4C                 move    $v0, $s0
    ROM:805DCD50
    ROM:805DCD50 loc_805DCD50:                            # CODE XREF: GetHeader+100↑j
    ROM:805DCD50                                          # GetHeader+114↑j
    ROM:805DCD50                 jal     FreeMemorySystem_Dup2
    ROM:805DCD54                 move    $a0, $s0
    ROM:805DCD58                 move    $a0, $s1
    ROM:805DCD5C
    ROM:805DCD5C loc_805DCD5C:                            # CODE XREF: GetHeader+8C↑j
    ROM:805DCD5C                                          # GetHeader+A0↑j ...
    ROM:805DCD5C                 jal     FreeMemory_Dup2
    ROM:805DCD60                 move    $a1, $zero
    ROM:805DCD64
    ROM:805DCD64 loc_805DCD64:                            # CODE XREF: GetHeader+1C↑j
    ROM:805DCD64                 move    $v0, $zero
    ROM:805DCD68
    ROM:805DCD68 loc_805DCD68:                            # CODE XREF: GetHeader+134↑j
    ROM:805DCD68                 lw      $ra, 0x20($sp)
    ROM:805DCD6C                 lw      $s3, 0x1C($sp)
    ROM:805DCD70                 lw      $s2, 0x18($sp)
    ROM:805DCD74                 lw      $s1, 0x14($sp)
    ROM:805DCD78                 lw      $s0, 0x10($sp)
    ROM:805DCD7C                 jr      $ra
    ROM:805DCD80                 addiu   $sp, 0x28
    ROM:805DCD80  # End of function GetHeader
    ROM:805DCD80
    """
    def is_proper(f, build_info):
        AUTODISK_FILEM_MAGIC = 0x39592841
        AUTODISK_FILED_MAGIC = 0x11993456
        CHECKSUM_OFFSET = 8

        metadata_magic = build_meta.read32bit(f, "big", build_info["autodisk_offset"])

        if metadata_magic == AUTODISK_FILEM_MAGIC:
            metadata_checksum = build_meta.read32bit(f, "big", build_info["autodisk_offset"] + 0x04)
            metadata_size = build_meta.read32bit(f, "big", build_info["autodisk_offset"] + 0x10)
            build_info["autodisk_file_count"] = build_meta.read32bit(f, "big", build_info["autodisk_offset"] + 0x14)
            
            if metadata_size > 0 and metadata_size < 0x10001 and build_info["autodisk_file_count"] > 0 and build_info["autodisk_file_count"] < 0x401:
                build_info["autodisk_filedata_offset"] = build_info["autodisk_offset"] + metadata_size

                filedata_magic = build_meta.read32bit(f, "big",  build_info["autodisk_filedata_offset"] - 4)

                if filedata_magic == AUTODISK_FILED_MAGIC:
                    f.seek(build_info["autodisk_offset"] + CHECKSUM_OFFSET)
                    data = bytes(f.read(metadata_size - CHECKSUM_OFFSET))

                    checksum = binascii.crc32(data, -1)

                    return True

        return False

    """
    ROM:805DC820 AutoDisk__ExtractFilesRead:              # CODE XREF: AutoDisk__Idle+64↓p
    ROM:805DC820                                          # AutoDisk__Initialize+64↓p
    ROM:805DC820                 addiu   $sp, -0xC8
    ROM:805DC824                 sw      $a0, 0xC8($sp)
    ROM:805DC828                 addiu   $a0, $sp, 0x10
    ROM:805DC82C                 sw      $ra, 0xC4($sp)
    ROM:805DC830                 sw      $fp, 0xC0($sp)
    ROM:805DC834                 sw      $s7, 0xBC($sp)
    ROM:805DC838                 sw      $s6, 0xB8($sp)
    ROM:805DC83C                 sw      $s5, 0xB4($sp)
    ROM:805DC840                 sw      $s4, 0xB0($sp)
    ROM:805DC844                 sw      $s3, 0xAC($sp)
    ROM:805DC848                 sw      $s2, 0xA8($sp)
    ROM:805DC84C                 sw      $s1, 0xA4($sp)
    ROM:805DC850                 sw      $s0, 0xA0($sp)
    ROM:805DC854                 sw      $zero, 0x88($sp)
    ROM:805DC858                 sw      $zero, 0x8C($sp)
    ROM:805DC85C                 jal     GroupDatabase
    ROM:805DC860                 sw      $zero, 0x90($sp)
    ROM:805DC864                 addiu   $s5, $sp, 0x28
    ROM:805DC868                 jal     Group
    ROM:805DC86C                 move    $a0, $s5
    ROM:805DC870                 jal     GroupDatabase__Load_Dup2
    ROM:805DC874                 addiu   $a0, $sp, 0x10
    ROM:805DC878                 bgez    $v0, loc_805DC888
    ROM:805DC87C                 li      $v0, 1
    ROM:805DC880                 j       loc_805DC930
    ROM:805DC884                 sw      $v0, 0x88($sp)
    ROM:805DC888  # ---------------------------------------------------------------------------
    ROM:805DC888
    ROM:805DC888 loc_805DC888:                            # CODE XREF: AutoDisk__ExtractFilesRead+58↑j
    ROM:805DC888                 jal     AutoDisk__GetVersion
    ROM:805DC88C                 nop
    ROM:805DC890                 move    $s0, $v0
    ROM:805DC894                 addiu   $a0, $sp, 0x10
    ROM:805DC898                 lui     $v0, 0x8077
    ROM:805DC89C                 addiu   $s1, $v0, (asc_8076F850 - 0x80770000)  # "AutoDisk"
    ROM:805DC8A0                 move    $a1, $s1
    ROM:805DC8A4                 jal     GroupDatabase__Find_
    ROM:805DC8A8                 move    $a2, $s5
    ROM:805DC8AC                 beqz    $v0, loc_805DC910
    ROM:805DC8B0                 lui     $v0, 0x8000
    ROM:805DC8B4                 lw      $v0, 0x80001700
    ROM:805DC8B8                 beqz    $v0, loc_805DC8DC
    ROM:805DC8BC                 lw      $v1, 0x3C($sp)
    ROM:805DC8C0                 li      $s0, 0x47726179
    ROM:805DC8C8                 move    $a0, $s5
    ROM:805DC8CC                 li      $a1, 2
    ROM:805DC8D0                 sw      $s0, 0x3C($sp)
    ROM:805DC8D4                 j       loc_805DC9D8
    ROM:805DC8D8                 sw      $zero, 0x34($sp)
    ROM:805DC8DC  # ---------------------------------------------------------------------------
    ROM:805DC8DC
    ROM:805DC8DC loc_805DC8DC:                            # CODE XREF: AutoDisk__ExtractFilesRead+98↑j
    ROM:805DC8DC                 beq     $v1, $s0, loc_805DC930
    ROM:805DC8E0                 li      $v0, 1
    ROM:805DC8E4                 sw      $v0, 0x8C($sp)
    ROM:805DC8E8                 li      $v0, 0x47726179
    ROM:805DC8F0                 beq     $v1, $v0, loc_805DC904
    ROM:805DC8F4                 sw      $s0, 0x3C($sp)
    ROM:805DC8F8                 li      $v1, 1
    ROM:805DC8FC                 j       loc_805DC930
    ROM:805DC900                 sw      $v1, 0x88($sp)
    ROM:805DC904  # ---------------------------------------------------------------------------
    ROM:805DC904
    ROM:805DC904 loc_805DC904:                            # CODE XREF: AutoDisk__ExtractFilesRead+D0↑j
    ROM:805DC904                 li      $v0, 1
    ROM:805DC908                 j       loc_805DC930
    ROM:805DC90C                 sw      $v0, 0x90($sp)
    ROM:805DC910  # ---------------------------------------------------------------------------
    ROM:805DC910
    ROM:805DC910 loc_805DC910:                            # CODE XREF: AutoDisk__ExtractFilesRead+8C↑j
    ROM:805DC910                 move    $a0, $s5
    ROM:805DC914                 jal     Group__SetName_
    ROM:805DC918                 move    $a1, $s1
    ROM:805DC91C                 li      $v1, 1
    ROM:805DC920                 sw      $v1, 0x88($sp)
    ROM:805DC924                 sw      $v1, 0x8C($sp)
    ROM:805DC928                 sw      $s0, 0x3C($sp)
    ROM:805DC92C                 sw      $zero, 0x34($sp)
    ROM:805DC930
    ROM:805DC930 loc_805DC930:                            # CODE XREF: AutoDisk__ExtractFilesRead+60↑j
    ROM:805DC930                                          # AutoDisk__ExtractFilesRead:loc_805DC8DC↑j ...
    ROM:805DC930                 jal     GetHeader
    ROM:805DC934                 nop
    ROM:805DC938                 move    $fp, $v0
    ROM:805DC93C                 beqz    $fp, loc_805DC9D0
    ROM:805DC940                 addiu   $s1, $fp, 0x18
    ROM:805DC944                 lw      $s3, 0x14($fp)
    ROM:805DC948                 sll     $v0, $s3, 2
    ROM:805DC94C                 addu    $v0, $s3
    ROM:805DC950                 sll     $v0, 2
    ROM:805DC954                 addu    $v0, $s1, $v0
    ROM:805DC958                 sw      $v0, 0x94($sp)
    ROM:805DC95C                 lw      $v0, 0x88($sp)
    ROM:805DC960                 beqz    $v0, loc_805DC97C
    ROM:805DC964                 sw      $zero, 0x98($sp)
    ROM:805DC968                 lw      $v1, 0xC8($sp)
    ROM:805DC96C                 bnez    $v1, loc_805DC980
    ROM:805DC970                 lui     $s0, 0x8000
    ROM:805DC974                 sw      $s3, 0x98($sp)
    ROM:805DC978                 move    $s3, $zero
    ROM:805DC97C
    ROM:805DC97C loc_805DC97C:                            # CODE XREF: AutoDisk__ExtractFilesRead+140↑j
    ROM:805DC97C                 lui     $s0, 0x8000
    ROM:805DC980
    ROM:805DC980 loc_805DC980:                            # CODE XREF: AutoDisk__ExtractFilesRead+14C↑j
    ROM:805DC980                 j       loc_805DC998
    ROM:805DC984                 lui     $v0, 2
    ROM:805DC988  # ---------------------------------------------------------------------------
    ROM:805DC988
    ROM:805DC988 loc_805DC988:                            # CODE XREF: AutoDisk__ExtractFilesRead+198↓j
    ROM:805DC988                 lw      $v0, 0x1B08($s0)
    ROM:805DC98C                 srl     $v1, $v0, 31
    ROM:805DC990                 addu    $v0, $v1
    ROM:805DC994                 sra     $v0, 1
    ROM:805DC998
    ROM:805DC998 loc_805DC998:                            # CODE XREF: AutoDisk__ExtractFilesRead:loc_805DC980↑j
    ROM:805DC998                 sw      $v0, 0x1B08($s0)
    ROM:805DC99C                 lw      $a0, 0x1B08($s0)
    ROM:805DC9A0                 slti    $v0, $a0, 0x400
    ROM:805DC9A4                 bnez    $v0, loc_805DC9C4
    ROM:805DC9A8                 lui     $v1, 0x8000
    ROM:805DC9AC                 jal     AllocateMemorySystemNilAllowed_Dup2
    ROM:805DC9B0                 nop
    ROM:805DC9B4                 lui     $v1, 0x8000
    ROM:805DC9B8                 beqz    $v0, loc_805DC988
    ROM:805DC9BC                 sw      $v0, 0x80001B04
    ROM:805DC9C0                 lui     $v1, 0x8000
    ROM:805DC9C4
    ROM:805DC9C4 loc_805DC9C4:                            # CODE XREF: AutoDisk__ExtractFilesRead+184↑j
    ROM:805DC9C4                 lw      $v0, 0x1B04($v1)
    ROM:805DC9C8                 bnez    $v0, loc_805DC9F4
    ROM:805DC9CC                 nop
    ROM:805DC9D0
    ROM:805DC9D0 loc_805DC9D0:                            # CODE XREF: AutoDisk__ExtractFilesRead+11C↑j
    ROM:805DC9D0                 move    $a0, $s5
    ROM:805DC9D4                 li      $a1, 2
    ROM:805DC9D8
    ROM:805DC9D8 loc_805DC9D8:                            # CODE XREF: AutoDisk__ExtractFilesRead+B4↑j
    ROM:805DC9D8                 jal     Group___Group
    ROM:805DC9DC                 nop
    ROM:805DC9E0                 addiu   $a0, $sp, 0x10
    ROM:805DC9E4                 jal     GroupDatabase___GroupDatabase
    ROM:805DC9E8                 li      $a1, 2
    ROM:805DC9EC                 j       loc_805DCBE4
    ROM:805DC9F0                 move    $v0, $zero
    ROM:805DC9F4  # ---------------------------------------------------------------------------
    ROM:805DC9F4
    ROM:805DC9F4 loc_805DC9F4:                            # CODE XREF: AutoDisk__ExtractFilesRead+1A8↑j
    ROM:805DC9F4                 blez    $s3, loc_805DCB60
    ROM:805DC9F8                 move    $s7, $zero
    ROM:805DC9FC                 move    $s6, $s1
    ROM:805DCA00
    ROM:805DCA00 loc_805DCA00:                            # CODE XREF: AutoDisk__ExtractFilesRead+338↓j
    ROM:805DCA00                 addiu   $s2, $sp, 0x40
    ROM:805DCA04                 lw      $v0, 0xC($s6)
    ROM:805DCA08                 lw      $v1, 0x94($sp)
    ROM:805DCA0C                 move    $a0, $s2
    ROM:805DCA10                 addu    $s4, $v1, $v0
    ROM:805DCA14                 jal     FSFile__FSFile_Dup2
    ROM:805DCA18                 move    $a1, $s4
    ROM:805DCA1C                 jal     FSItem__Exists_Dup2
    ROM:805DCA20                 move    $a0, $s2
    ROM:805DCA24                 beqz    $v0, loc_805DCA84
    ROM:805DCA28                 lw      $v0, 0x88($sp)
    ROM:805DCA2C                 beqz    $v0, loc_805DCA84
    ROM:805DCA30                 lw      $v1, 0xC8($sp)
    ROM:805DCA34                 beqz    $v1, loc_805DCA7C
    ROM:805DCA38                 lw      $v0, 0x98($sp)
    ROM:805DCA3C                 jal     Remove
    ROM:805DCA40                 move    $a0, $s2
    ROM:805DCA44                 jal     sub_80725C64
    ROM:805DCA48                 move    $a0, $s2
    ROM:805DCA4C                 addiu   $s0, $sp, 0x58
    ROM:805DCA50                 move    $a0, $s0
    ROM:805DCA54                 jal     FSPath__FSPath_Dup204
    ROM:805DCA58                 move    $a1, $s4
    ROM:805DCA5C                 move    $a0, $s2
    ROM:805DCA60                 jal     FSItem__SetPath
    ROM:805DCA64                 move    $a1, $s0
    ROM:805DCA68                 move    $a0, $s0
    ROM:805DCA6C                 jal     FSPath___FSPath
    ROM:805DCA70                 li      $a1, 2
    ROM:805DCA74                 j       loc_805DCA84
    ROM:805DCA78                 nop
    ROM:805DCA7C  # ---------------------------------------------------------------------------
    ROM:805DCA7C
    ROM:805DCA7C loc_805DCA7C:                            # CODE XREF: AutoDisk__ExtractFilesRead+214↑j
    ROM:805DCA7C                 addiu   $v0, 1
    ROM:805DCA80                 sw      $v0, 0x98($sp)
    ROM:805DCA84
    ROM:805DCA84 loc_805DCA84:                            # CODE XREF: AutoDisk__ExtractFilesRead+204↑j
    ROM:805DCA84                                          # AutoDisk__ExtractFilesRead+20C↑j ...
    ROM:805DCA84                 jal     FSItem__Exists_Dup2
    ROM:805DCA88                 move    $a0, $s2
    ROM:805DCA8C                 bnez    $v0, loc_805DCB34
    ROM:805DCA90                 lw      $v1, 0xC8($sp)
    ROM:805DCA94                 beqz    $v1, loc_805DCB24
    ROM:805DCA98                 addiu   $s0, $sp, 0x58
    ROM:805DCA9C                 move    $a0, $s0
    ROM:805DCAA0                 lui     $a1, 0x8077
    ROM:805DCAA4                 jal     FSDirectory__FSDirectory_Dup934
    ROM:805DCAA8                 la      $a1, asc_8076F85C  # "/"
    ROM:805DCAAC                 addiu   $s1, $sp, 0x70
    ROM:805DCAB0                 move    $a0, $s1
    ROM:805DCAB4                 jal     FSPath__FSPath_Dup204
    ROM:805DCAB8                 move    $a1, $s4
    ROM:805DCABC                 move    $a0, $s0
    ROM:805DCAC0                 move    $a1, $s1
    ROM:805DCAC4                 move    $a2, $zero
    ROM:805DCAC8                 jal     FSDirectory__Create
    ROM:805DCACC                 li      $a3, 1
    ROM:805DCAD0                 move    $a0, $s1
    ROM:805DCAD4                 jal     FSPath___FSPath
    ROM:805DCAD8                 li      $a1, 2
    ROM:805DCADC                 jal     sub_80725C64
    ROM:805DCAE0                 move    $a0, $s2
    ROM:805DCAE4                 move    $a0, $s1
    ROM:805DCAE8                 jal     FSPath__FSPath_Dup204
    ROM:805DCAEC                 move    $a1, $s4
    ROM:805DCAF0                 move    $a0, $s2
    ROM:805DCAF4                 jal     FSItem__SetPath
    ROM:805DCAF8                 move    $a1, $s1
    ROM:805DCAFC                 move    $a0, $s1
    ROM:805DCB00                 jal     FSPath___FSPath
    ROM:805DCB04                 li      $a1, 2
    ROM:805DCB08                 move    $a0, $s2
    ROM:805DCB0C                 move    $a1, $fp
    ROM:805DCB10                 jal     AutoDisk__InstallFile
    ROM:805DCB14                 move    $a2, $s6
    ROM:805DCB18                 move    $a0, $s0
    ROM:805DCB1C                 jal     FSDirectory___FSDirectory
    ROM:805DCB20                 li      $a1, 2
    ROM:805DCB24
    ROM:805DCB24 loc_805DCB24:                            # CODE XREF: AutoDisk__ExtractFilesRead+274↑j
    ROM:805DCB24                 lw      $v0, 0x98($sp)
    ROM:805DCB28                 addiu   $v0, 1
    ROM:805DCB2C                 sw      $v0, 0x98($sp)
    ROM:805DCB30                 lw      $v1, 0xC8($sp)
    ROM:805DCB34
    ROM:805DCB34 loc_805DCB34:                            # CODE XREF: AutoDisk__ExtractFilesRead+26C↑j
    ROM:805DCB34                 beqz    $v1, loc_805DCB44
    ROM:805DCB38                 addiu   $a0, $s7, 1
    ROM:805DCB3C                 jal     AutoDisk__UpdateUserInterface
    ROM:805DCB40                 move    $a1, $s3
    ROM:805DCB44
    ROM:805DCB44 loc_805DCB44:                            # CODE XREF: AutoDisk__ExtractFilesRead:loc_805DCB34↑j
    ROM:805DCB44                 move    $a0, $s2
    ROM:805DCB48                 jal     FSFile___FSFile
    ROM:805DCB4C                 li      $a1, 2
    ROM:805DCB50                 addiu   $s7, 1
    ROM:805DCB54                 slt     $v0, $s7, $s3
    ROM:805DCB58                 bnez    $v0, loc_805DCA00
    ROM:805DCB5C                 addiu   $s6, 0x14
    ROM:805DCB60
    ROM:805DCB60 loc_805DCB60:                            # CODE XREF: AutoDisk__ExtractFilesRead:loc_805DC9F4↑j
    ROM:805DCB60                 jal     FreeMemorySystem_Dup2
    ROM:805DCB64                 move    $a0, $fp
    ROM:805DCB68                 lui     $v0, 0x8000
    ROM:805DCB6C                 jal     FreeMemorySystem_Dup2
    ROM:805DCB70                 lw      $a0, 0x80001B04
    ROM:805DCB74                 lw      $v1, 0x8C($sp)
    ROM:805DCB78                 beqz    $v1, loc_805DCBC8
    ROM:805DCB7C                 lw      $v0, 0xC8($sp)
    ROM:805DCB80                 bnez    $v0, loc_805DCBA0
    ROM:805DCB84                 li      $v0, 1
    ROM:805DCB88                 lw      $v1, 0x98($sp)
    ROM:805DCB8C                 bnezl   $v1, loc_805DCBCC
    ROM:805DCB90                 addiu   $a0, $sp, 0x28
    ROM:805DCB94                 lw      $v0, 0x90($sp)
    ROM:805DCB98                 beqz    $v0, loc_805DCBC8
    ROM:805DCB9C                 li      $v0, 1
    ROM:805DCBA0
    ROM:805DCBA0 loc_805DCBA0:                            # CODE XREF: AutoDisk__ExtractFilesRead+360↑j
    ROM:805DCBA0                 sb      $v0, 0x30($sp)
    ROM:805DCBA4                 move    $a0, $s5
    ROM:805DCBA8                 lui     $a1, 0x8077
    ROM:805DCBAC                 jal     SetBase
    ROM:805DCBB0                 la      $a1, 0x8076F860  # "file://Disk/Browser/AutoDisk/"
    ROM:805DCBB4                 addiu   $a0, $sp, 0x10
    ROM:805DCBB8                 jal     GroupDatabase__Put_Dup2
    ROM:805DCBBC                 move    $a1, $s5
    ROM:805DCBC0                 jal     Store
    ROM:805DCBC4                 addiu   $a0, $sp, 0x10
    ROM:805DCBC8
    ROM:805DCBC8 loc_805DCBC8:                            # CODE XREF: AutoDisk__ExtractFilesRead+358↑j
    ROM:805DCBC8                                          # AutoDisk__ExtractFilesRead+378↑j
    ROM:805DCBC8                 addiu   $a0, $sp, 0x28
    ROM:805DCBCC
    ROM:805DCBCC loc_805DCBCC:                            # CODE XREF: AutoDisk__ExtractFilesRead+36C↑j
    ROM:805DCBCC                 jal     Group___Group
    ROM:805DCBD0                 li      $a1, 2
    ROM:805DCBD4                 addiu   $a0, $sp, 0x10
    ROM:805DCBD8                 jal     GroupDatabase___GroupDatabase
    ROM:805DCBDC                 li      $a1, 2
    ROM:805DCBE0                 lw      $v0, 0x98($sp)
    ROM:805DCBE4
    ROM:805DCBE4 loc_805DCBE4:                            # CODE XREF: AutoDisk__ExtractFilesRead+1CC↑j
    ROM:805DCBE4                 lw      $ra, 0xC4($sp)
    ROM:805DCBE8                 lw      $fp, 0xC0($sp)
    ROM:805DCBEC                 lw      $s7, 0xBC($sp)
    ROM:805DCBF0                 lw      $s6, 0xB8($sp)
    ROM:805DCBF4                 lw      $s5, 0xB4($sp)
    ROM:805DCBF8                 lw      $s4, 0xB0($sp)
    ROM:805DCBFC                 lw      $s3, 0xAC($sp)
    ROM:805DCC00                 lw      $s2, 0xA8($sp)
    ROM:805DCC04                 lw      $s1, 0xA4($sp)
    ROM:805DCC08                 lw      $s0, 0xA0($sp)
    ROM:805DCC0C                 jr      $ra
    ROM:805DCC10                 addiu   $sp, 0xC8
    ROM:805DCC10  # End of function AutoDisk__ExtractFilesRead
    """
    def walk(origin, callback, read_data = True):
        if callback != None:
            build_info = build_meta.detect(origin)
            build_meta.print_build_info(build_info)

            with open(build_info["path"], "rb") as f:
                if autodisk.is_proper(f, build_info):

                    for i in range(0, build_info["autodisk_file_count"]):
                        f.seek(build_info["autodisk_offset"] + 0x18 + (0x14 * i))
                        file_info = struct.unpack_from(">IIIII", bytes(f.read(0x14)))

                        f.seek(build_info["autodisk_offset"] + 0x19 + (0x14 * build_info["autodisk_file_count"]) + file_info[3])
                        _path = struct.unpack_from(">255s", bytes(f.read(0xFF)))[0]
                        path = str(_path[0:_path.index(b'\x00')], "ascii", "ignore")

                        data = None
                        if read_data:
                            f.seek(build_info["autodisk_filedata_offset"] + file_info[2])
                            data = bytes(f.read(file_info[1]))

                        autodisk_node = {
                            "unknown_x": file_info[0],
                            "size": file_info[1],
                            "filedata_offset": file_info[2],
                            "filename_offset": file_info[3],
                            "data_checksum": file_info[4],
                            "data": data,
                            "path": path,
                            "name": os.path.basename(path),
                        }

                        callback(autodisk_node)

                f.close()

    def list(origin, simplify_sizes = False, read_data = False):
        def _list(autodisk_node):
            size = "0B"
            if simplify_sizes:
                size = romfs_explode.simplify_size(autodisk_node["size"])
            else:
                size = str(autodisk_node["size"]) + "B"

            print(autodisk_node["path"] + "\t(" + size + ")")

        autodisk.walk(origin, _list)


    def unpack(origin, destination = "./out"):
        if not os.path.isdir(destination):
            os.mkdir(destination)

            if not os.path.isdir(destination):
                raise Exception("Destination doesn't exist")

        def _unpack(autodisk_node):
            path = destination + "/" + autodisk_node["path"]

            print("\tUnpack: " + autodisk_node["path"])

            dir = os.path.dirname(path)
            if not os.path.isdir(dir):
                os.makedirs(dir)

            with open(path, "wb") as f:
                f.write(autodisk_node["data"])
                f.close()

        autodisk.walk(origin, _unpack)
