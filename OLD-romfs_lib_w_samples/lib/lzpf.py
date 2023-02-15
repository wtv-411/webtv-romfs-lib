import ctypes

class lzpf():
    debug = False

    decode = {
        "current_data": 0,
        "current_width": 0,
        "flags_table": [],
        "codes": 
        [
            [
                0x00000000, 0x80000000, 0xC0000000,
                0xE0000000, 0xF0000000, 0xF8000000,
                0xFC000000, 0xFE000000, 0xFF000000,
                0xFF800000, 0xFFC00000, 0xFFE00000,
                0xFFF00000, 0xFFF80000, 0xFFFC0000,
                0xFFFE0000, 0xFFFF0000, 0xFFFF8000,
                0xFFFFC000, 0xFFFFE000, 0xFFFFF000,
                0xFFFFF800, 0xFFFFFC00, 0xFFFFFE00,
                0xFFFFFF00, 0xFFFFFF80, 0xFFFFFFC0,
                0xFFFFFFE0, 0xFFFFFFF0, 0xFFFFFFF8,
                0xFFFFFFFC, 0xFFFFFFFE, 0xFFFFFFFF
            ],
            [
                0x20, 0x65, 0x0A, 0x22, 0x2F, 0x3C, 0x3E, 0x54,
                0x61, 0x69, 0x6E, 0x6F, 0x70, 0x72, 0x73, 0x74,
                0x09, 0x2E, 0x3D, 0x41, 0x45, 0x49, 0x4E, 0x4F,
                0x52, 0x63, 0x64, 0x68, 0x6C, 0x6D, 0x77, 0x2C,
                0x2D, 0x31, 0x42, 0x43, 0x44, 0x46, 0x47, 0x48,
                0x4C, 0x50, 0x53, 0x62, 0x66, 0x67, 0x75, 0x30,
                0x32, 0x34, 0x3A, 0x4D, 0x57, 0x5F, 0x6B, 0x76,
                0x79, 0x0D, 0x23, 0x27, 0x33, 0x35, 0x36, 0x37,
                0x38, 0x39, 0x55, 0x56, 0x5A, 0x78, 0x21, 0x2A,
                0x3F, 0x4B, 0x59, 0x7A, 0x26, 0x28, 0x29, 0x3B,
                0x4A, 0x6A, 0x71, 0x51, 0x58, 0x7B, 0x7C, 0x7D,
                0x7E, 0x2B, 0x24, 0x40, 0x05, 0x07, 0x08, 0x0B,
                0x17, 0x91, 0x92, 0x93, 0xC7, 0xF3, 0xFA, 0x00,
                0x01, 0x02, 0x03, 0x04, 0x06, 0x0C, 0x0E, 0x0F,
                0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x18,
                0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x25,
                0x5B, 0x5C, 0x5D, 0x5E, 0x60, 0x7F, 0x80, 0x81,
                0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
                0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90, 0x94,
                0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x9C,
                0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4,
                0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC,
                0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4,
                0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC,
                0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4,
                0xC5, 0xC6, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD,
                0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5,
                0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD,
                0xDE, 0xDF, 0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5,
                0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED,
                0xEE, 0xEF, 0xF0, 0xF1, 0xF2, 0xF4, 0xF5, 0xF6,
                0xF7, 0xF8, 0xF9, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF
            ],
            [
                0x00, 0x02, 0x04, 0x08, 0x0E, 0x0E, 0x0D, 0x0A,
                0x0A, 0x07, 0x08, 0x09, 0x0C, 0x17, 0x2C, 0x4D,
                0x00, 0x00, 0x00, 0x00,
            ],
            [
                0x00, 0xFE, 0xFC, 0xF8, 0xF2, 0xF4, 0x03, 0x15,
                0x25, 0x32, 0x3E, 0x43, 0x47, 0x42, 0x2E, 0x0F,
                0x67, 0x00, 0x00, 0x00
            ]
        ],

        "code_widths":
        [
            [
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09,
                0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09,
                0x09, 0x09, 0x09, 0x09, 0x08, 0x08, 0x08, 0x08,
                0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
                0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04,
                0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04
            ],
            [
                0x01, 0x03, 0x01, 0x03, 0x01, 0x03, 0x01, 0x03,
                0x01, 0x03, 0x01, 0x03, 0x01, 0x03, 0x01, 0x03, 
                0x02, 0x03, 0x02, 0x03, 0x02, 0x03, 0x02, 0x03,
                0x02, 0x03, 0x02, 0x03, 0x02, 0x03, 0x02, 0x03, 
                0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,
                0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 
                0x04, 0x06, 0x05, 0x06, 0x06, 0x06, 0x07, 0x06,
                0x08, 0x06, 0x09, 0x06, 0x0A, 0x06, 0x00, 0x00
            ]
        ]
    }

    """
    ROM:804A8550 Lzpf_Init:                               # CODE XREF: CompressionLzpfStream__BeginWriting+1C↑p
    ROM:804A8550                                          # GetFileData+22C↓p
    ROM:804A8550
    ROM:804A8550 var_18          = -0x18
    ROM:804A8550 var_14          = -0x14
    ROM:804A8550 var_10          = -0x10
    ROM:804A8550 var_C           = -0xC
    ROM:804A8550 var_8           = -8
    ROM:804A8550
    ROM:804A8550                 addiu   $sp, -0x28
    ROM:804A8554                 sw      $s1, 0x28+var_14($sp)
    ROM:804A8558                 sw      $s3, 0x28+var_C($sp)
    ROM:804A855C                 sw      $s2, 0x28+var_10($sp)
    ROM:804A8560                 move    $s1, $a0
    ROM:804A8564                 sw      $s0, 0x28+var_18($sp)
    ROM:804A8568                 sw      $ra, 0x28+var_8($sp)
    ROM:804A856C                 move    $s2, $a1
    ROM:804A8570                 move    $s3, $a2
    ROM:804A8574                 jal     AllocateMemorySystemZeroNilAllowed
    ROM:804A8578                 li      $a0, 0x64
    ROM:804A857C                 move    $s0, $v0
    ROM:804A8580                 beqz    $s0, loc_804A85E4
    ROM:804A8584                 move    $v0, $zero
    ROM:804A8588                 sb      $s1, 0($s0)
    ROM:804A858C                 sw      $s2, 4($s0)
    ROM:804A8590                 sw      $s3, 8($s0)
    ROM:804A8594                 jal     AllocateMemorySystem
    ROM:804A8598                 li      $a0, 0x2000
    ROM:804A859C                 beqz    $v0, loc_804A85D8
    ROM:804A85A0                 sw      $v0, 0x40($s0)
    ROM:804A85A4                 jal     AllocateMemorySystem
    ROM:804A85A8                 li      $a0, 0x2000
    ROM:804A85AC                 beqz    $v0, loc_804A85D0
    ROM:804A85B0                 sw      $v0, 0x50($s0)
    ROM:804A85B4                 move    $a0, $v0
    ROM:804A85B8                 li      $a1, 0xFF
    ROM:804A85BC                 jal     wtv_memset
    ROM:804A85C0                 li      $a2, 0x2000
    ROM:804A85C4                 move    $v0, $s0
    ROM:804A85C8                 j       loc_804A85E4
    ROM:804A85CC                 sh      $zero, 0x1C($s0)
    ROM:804A85D0  # ---------------------------------------------------------------------------
    ROM:804A85D0
    ROM:804A85D0 loc_804A85D0:                            # CODE XREF: Lzpf_Init+5C↑j
    ROM:804A85D0                 jal     FreeMemorySystem
    ROM:804A85D4                 lw      $a0, 0x40($s0)
    ROM:804A85D8
    ROM:804A85D8 loc_804A85D8:                            # CODE XREF: Lzpf_Init+4C↑j
    ROM:804A85D8                 jal     FreeMemorySystem
    ROM:804A85DC                 move    $a0, $s0
    ROM:804A85E0                 move    $v0, $zero
    ROM:804A85E4
    ROM:804A85E4 loc_804A85E4:                            # CODE XREF: Lzpf_Init+30↑j
    ROM:804A85E4                                          # Lzpf_Init+78↑j
    ROM:804A85E4                 lw      $ra, 0x28+var_8($sp)
    ROM:804A85E8                 lw      $s3, 0x28+var_C($sp)
    ROM:804A85EC                 lw      $s2, 0x28+var_10($sp)
    ROM:804A85F0                 lw      $s1, 0x28+var_14($sp)
    ROM:804A85F4                 lw      $s0, 0x28+var_18($sp)
    ROM:804A85F8                 jr      $ra
    ROM:804A85FC                 addiu   $sp, 0x28
    ROM:804A85FC  # End of function Lzpf_Init
    """
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.decode["current_width"] = ctypes.c_int32(0)
        self.decode["current_data"] = ctypes.c_uint32(0)
        self.decode["flags_table"] = [0xFFFF] * 0x1000

    """
    ROM:804A86B8 Lzpf_Expand:                             # CODE XREF: CompressionLzpfStream__Write+68↑p
    ROM:804A86B8                                          # GetFileData+258↓p
    ROM:804A86B8
    ROM:804A86B8 var_28          = -0x28
    ROM:804A86B8 var_20          = -0x20
    ROM:804A86B8 var_1C          = -0x1C
    ROM:804A86B8 var_18          = -0x18
    ROM:804A86B8 var_14          = -0x14
    ROM:804A86B8 var_10          = -0x10
    ROM:804A86B8 var_C           = -0xC
    ROM:804A86B8 var_8           = -8
    ROM:804A86B8 var_4           = -4
    ROM:804A86B8 arg_4           =  4
    ROM:804A86B8 arg_8           =  8
    ROM:804A86B8
    ROM:804A86B8                 addiu   $sp, -0x38
    ROM:804A86BC                 sw      $s3, 0x38+var_14($sp)
    ROM:804A86C0                 sw      $s2, 0x38+var_18($sp)
    ROM:804A86C4                 sw      $ra, 0x38+var_4($sp)
    ROM:804A86C8                 sw      $s6, 0x38+var_8($sp)
    ROM:804A86CC                 sw      $s5, 0x38+var_C($sp)
    ROM:804A86D0                 sw      $s4, 0x38+var_10($sp)
    ROM:804A86D4                 sw      $s1, 0x38+var_1C($sp)
    ROM:804A86D8                 sw      $s0, 0x38+var_20($sp)
    ROM:804A86DC                 move    $s3, $a0
    ROM:804A86E0                 sw      $a1, 0x38+arg_4($sp)
    ROM:804A86E4                 sw      $a2, 0x38+arg_8($sp)
    ROM:804A86E8                 move    $s2, $a3
    ROM:804A86EC                 beqz    $s3, loc_804A8ACC
    ROM:804A86F0                 li      $v0, 0xFFFFFFFF
    ROM:804A86F4                 lbu     $v0, 0x58($s3)
    ROM:804A86F8                 lhu     $s5, 0x1C($s3)
    ROM:804A86FC                 move    $s6, $s2
    ROM:804A8700                 lw      $s1, 0x44($s3)
    ROM:804A8704                 beqz    $v0, loc_804A8718
    ROM:804A8708                 lw      $s4, 0x3C($s3)
    ROM:804A870C                 lbu     $v0, 0x59($s3)
    ROM:804A8710                 sb      $v0, 0($s2)
    ROM:804A8714                 addiu   $s2, 1
    ROM:804A8718
    ROM:804A8718 loc_804A8718:                            # CODE XREF: Lzpf_Expand+4C↑j
    ROM:804A8718                 lw      $v1, 0x38($s3)
    ROM:804A871C                 li      $s0, 3
    ROM:804A8720                 beq     $v1, $s0, loc_804A89E0
    ROM:804A8724                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8728                 slti    $v0, $v1, 5
    ROM:804A872C                 bnez    $v0, loc_804A8780
    ROM:804A8730                 slti    $v0, $v1, 3
    ROM:804A8734                 move    $a0, $s3
    ROM:804A8738                 addiu   $a1, $sp, 0x38+arg_8
    ROM:804A873C                 jal     CheckPartialChecksum
    ROM:804A8740                 addiu   $a2, $sp, 0x38+arg_4
    ROM:804A8744                 bgezl   $v0, loc_804A8768
    ROM:804A8748                 lw      $v1, 0x54($s3)
    ROM:804A874C                 break   0
    ROM:804A8750                 lw      $v1, 0x54($s3)
    ROM:804A8754                 lw      $a0, 0x38+arg_8($sp)
    ROM:804A8758                 li      $v0, 0xFFFFFFFF
    ROM:804A875C                 addu    $v1, $a0
    ROM:804A8760                 j       loc_804A8ACC
    ROM:804A8764                 sw      $v1, 0x54($s3)
    ROM:804A8768  # ---------------------------------------------------------------------------
    ROM:804A8768
    ROM:804A8768 loc_804A8768:                            # CODE XREF: Lzpf_Expand+8C↑j
    ROM:804A8768                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A876C                 addu    $v0, $v1, $v0
    ROM:804A8770                 bne     $v0, $s0, loc_804A8A8C
    ROM:804A8774                 sw      $v0, 0x54($s3)
    ROM:804A8778                 j       loc_804A8A74
    ROM:804A877C                 lw      $v1, 0x38($s3)
    ROM:804A8780  # ---------------------------------------------------------------------------
    ROM:804A8780
    ROM:804A8780 loc_804A8780:                            # CODE XREF: Lzpf_Expand+74↑j
    ROM:804A8780                 beqz    $v0, loc_804A8864
    ROM:804A8784                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8788
    ROM:804A8788 loc_804A8788:                            # CODE XREF: Lzpf_Expand+190↓j
    ROM:804A8788                 li      $v1, 0xFFFFFFFF
    ROM:804A878C                 addiu   $v0, -1
    ROM:804A8790                 beq     $v0, $v1, loc_804A8850
    ROM:804A8794                 sw      $v0, 0x38+arg_8($sp)
    ROM:804A8798                 lw      $a1, 0x38+arg_4($sp)
    ROM:804A879C                 lw      $a2, 0x10($s3)
    ROM:804A87A0                 lbu     $v1, 0($a1)
    ROM:804A87A4                 li      $v0, 0x18
    ROM:804A87A8                 subu    $v0, $a2
    ROM:804A87AC                 lw      $a0, 0xC($s3)
    ROM:804A87B0                 sllv    $v1, $v0
    ROM:804A87B4                 or      $a0, $v1
    ROM:804A87B8                 lw      $v0, 0x38($s3)
    ROM:804A87BC                 addiu   $a1, 1
    ROM:804A87C0                 sw      $a0, 0xC($s3)
    ROM:804A87C4                 addiu   $a2, 8
    ROM:804A87C8                 sw      $a1, 0x38+arg_4($sp)
    ROM:804A87CC                 slti    $v0, 3
    ROM:804A87D0                 beqz    $v0, loc_804A8860
    ROM:804A87D4                 sw      $a2, 0x10($s3)
    ROM:804A87D8
    ROM:804A87D8 loc_804A87D8:                            # CODE XREF: Lzpf_Expand+180↓j
    ROM:804A87D8                 lw      $v0, 0x10($s3)
    ROM:804A87DC                 slti    $v0, 0x13
    ROM:804A87E0                 bnez    $v0, loc_804A8840
    ROM:804A87E4                 move    $a1, $zero
    ROM:804A87E8                 move    $a0, $s3
    ROM:804A87EC                 jal     HuffDecodeLiteralNoFlags
    ROM:804A87F0                 move    $a2, $s2
    ROM:804A87F4                 li      $v1, 0xFFFFFFFE
    ROM:804A87F8                 beq     $v0, $v1, loc_804A8A04
    ROM:804A87FC                 li      $v0, 5
    ROM:804A8800                 lw      $v0, 0x40($s3)
    ROM:804A8804                 lbu     $v1, 0($s2)
    ROM:804A8808                 lbu     $a1, 0($s2)
    ROM:804A880C                 addu    $v0, $s1
    ROM:804A8810                 sb      $v1, 0($v0)
    ROM:804A8814                 lw      $a0, 0x38($s3)
    ROM:804A8818                 sll     $v0, $s4, 8
    ROM:804A881C                 addiu   $a0, 1
    ROM:804A8820                 addu    $v1, $s5, $v1
    ROM:804A8824                 addu    $s4, $v0, $a1
    ROM:804A8828                 andi    $s5, $v1, 0xFFFF
    ROM:804A882C                 slti    $v0, $a0, 3
    ROM:804A8830                 addiu   $s1, 1
    ROM:804A8834                 addiu   $s2, 1
    ROM:804A8838                 bnez    $v0, loc_804A87D8
    ROM:804A883C                 sw      $a0, 0x38($s3)
    ROM:804A8840
    ROM:804A8840 loc_804A8840:                            # CODE XREF: Lzpf_Expand+128↑j
    ROM:804A8840                 lw      $v0, 0x38($s3)
    ROM:804A8844                 slti    $v0, 3
    ROM:804A8848                 bnez    $v0, loc_804A8788
    ROM:804A884C                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8850
    ROM:804A8850 loc_804A8850:                            # CODE XREF: Lzpf_Expand+D8↑j
    ROM:804A8850                 lw      $v0, 0x38($s3)
    ROM:804A8854                 slti    $v0, 3
    ROM:804A8858                 bnez    $v0, loc_804A887C
    ROM:804A885C                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8860
    ROM:804A8860 loc_804A8860:                            # CODE XREF: Lzpf_Expand+118↑j
    ROM:804A8860                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8864
    ROM:804A8864 loc_804A8864:                            # CODE XREF: Lzpf_Expand:loc_804A8780↑j
    ROM:804A8864                 bnez    $v0, loc_804A89D0
    ROM:804A8868                 lw      $v0, 0x10($s3)
    ROM:804A886C                 slti    $v0, 0x13
    ROM:804A8870                 beqz    $v0, loc_804A88C8
    ROM:804A8874                 srl     $v0, $s4, 11
    ROM:804A8878                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A887C
    ROM:804A887C loc_804A887C:                            # CODE XREF: Lzpf_Expand+1A0↑j
    ROM:804A887C                 bnezl   $v0, loc_804A89F4
    ROM:804A8880                 sw      $s1, 0x44($s3)
    ROM:804A8884                 li      $v0, 0xFFFFFFFF
    ROM:804A8888                 j       loc_804A89F0
    ROM:804A888C                 sw      $v0, 0x38+arg_8($sp)
    ROM:804A8890  # ---------------------------------------------------------------------------
    ROM:804A8890
    ROM:804A8890 loc_804A8890:                            # CODE XREF: Lzpf_Expand+330↓j
    ROM:804A8890                 lw      $a1, 0x38+arg_4($sp)
    ROM:804A8894                 lw      $a2, 0x10($s3)
    ROM:804A8898                 lbu     $v1, 0($a1)
    ROM:804A889C                 li      $v0, 0x18
    ROM:804A88A0                 lw      $a0, 0xC($s3)
    ROM:804A88A4                 subu    $v0, $a2
    ROM:804A88A8                 sllv    $v1, $v0
    ROM:804A88AC                 or      $a0, $v1
    ROM:804A88B0                 addiu   $a1, 1
    ROM:804A88B4                 sw      $a0, 0xC($s3)
    ROM:804A88B8                 addiu   $a2, 8
    ROM:804A88BC                 sw      $a1, 0x38+arg_4($sp)
    ROM:804A88C0                 j       loc_804A89CC
    ROM:804A88C4                 sw      $a2, 0x10($s3)
    ROM:804A88C8  # ---------------------------------------------------------------------------
    ROM:804A88C8
    ROM:804A88C8 loc_804A88C8:                            # CODE XREF: Lzpf_Expand+1B8↑j
    ROM:804A88C8                                          # Lzpf_Expand+31C↓j
    ROM:804A88C8                 xor     $v0, $s4
    ROM:804A88CC                 lw      $v1, 0x50($s3)
    ROM:804A88D0                 andi    $v0, 0xFFF
    ROM:804A88D4                 sll     $v0, 1
    ROM:804A88D8                 addu    $v0, $v1
    ROM:804A88DC                 lhu     $s0, 0($v0)
    ROM:804A88E0                 sh      $s1, 0($v0)
    ROM:804A88E4                 li      $v0, 0xFFFF
    ROM:804A88E8                 beq     $s0, $v0, loc_804A8988
    ROM:804A88EC                 move    $a0, $s3
    ROM:804A88F0                 lw      $v0, 0xC($s3)
    ROM:804A88F4                 bgez    $v0, loc_804A8978
    ROM:804A88F8                 move    $a1, $zero
    ROM:804A88FC                 move    $a0, $s3
    ROM:804A8900                 jal     ReadMatch
    ROM:804A8904                 addiu   $a2, $sp, 0x38+var_28
    ROM:804A8908                 lw      $v0, 0x38+var_28($sp)
    ROM:804A890C                 li      $v1, 0xFFFFFFFF
    ROM:804A8910                 addiu   $v0, -1
    ROM:804A8914                 beq     $v0, $v1, loc_804A89CC
    ROM:804A8918                 sw      $v0, 0x38+var_28($sp)
    ROM:804A891C
    ROM:804A891C loc_804A891C:                            # CODE XREF: Lzpf_Expand+2B0↓j
    ROM:804A891C                 lw      $v1, 0x40($s3)
    ROM:804A8920                 sll     $a2, $s4, 8
    ROM:804A8924                 addu    $v0, $v1, $s0
    ROM:804A8928                 lbu     $a0, 0($v0)
    ROM:804A892C                 lbu     $a1, 0($v0)
    ROM:804A8930                 addu    $v1, $s1
    ROM:804A8934                 sb      $a0, 0($v1)
    ROM:804A8938                 lw      $v1, 0x38+var_28($sp)
    ROM:804A893C                 addu    $v0, $s5, $a0
    ROM:804A8940                 sb      $a0, 0($s2)
    ROM:804A8944                 addiu   $v1, -1
    ROM:804A8948                 addiu   $s0, 1
    ROM:804A894C                 addiu   $s1, 1
    ROM:804A8950                 andi    $s5, $v0, 0xFFFF
    ROM:804A8954                 addu    $s4, $a2, $a1
    ROM:804A8958                 addiu   $s2, 1
    ROM:804A895C                 andi    $s0, 0x1FFF
    ROM:804A8960                 andi    $s1, 0x1FFF
    ROM:804A8964                 li      $v0, 0xFFFFFFFF
    ROM:804A8968                 bne     $v1, $v0, loc_804A891C
    ROM:804A896C                 sw      $v1, 0x38+var_28($sp)
    ROM:804A8970                 j       loc_804A89D0
    ROM:804A8974                 lw      $v0, 0x10($s3)
    ROM:804A8978  # ---------------------------------------------------------------------------
    ROM:804A8978
    ROM:804A8978 loc_804A8978:                            # CODE XREF: Lzpf_Expand+23C↑j
    ROM:804A8978                 jal     HuffDecodeLiteral
    ROM:804A897C                 move    $a2, $s2
    ROM:804A8980                 j       loc_804A8998
    ROM:804A8984                 li      $v1, 0xFFFFFFFE
    ROM:804A8988  # ---------------------------------------------------------------------------
    ROM:804A8988
    ROM:804A8988 loc_804A8988:                            # CODE XREF: Lzpf_Expand+230↑j
    ROM:804A8988                 move    $a1, $zero
    ROM:804A898C                 jal     HuffDecodeLiteralNoFlags
    ROM:804A8990                 move    $a2, $s2
    ROM:804A8994                 li      $v1, 0xFFFFFFFE
    ROM:804A8998
    ROM:804A8998 loc_804A8998:                            # CODE XREF: Lzpf_Expand+2C8↑j
    ROM:804A8998                 beq     $v0, $v1, loc_804A8A00
    ROM:804A899C                 sll     $v0, $s4, 8
    ROM:804A89A0                 lw      $v1, 0x40($s3)
    ROM:804A89A4                 lbu     $a0, 0($s2)
    ROM:804A89A8                 lbu     $a1, 0($s2)
    ROM:804A89AC                 addu    $v1, $s1
    ROM:804A89B0                 addu    $a2, $s5, $a0
    ROM:804A89B4                 addiu   $s1, 1
    ROM:804A89B8                 addu    $s4, $v0, $a1
    ROM:804A89BC                 sb      $a0, 0($v1)
    ROM:804A89C0                 andi    $s5, $a2, 0xFFFF
    ROM:804A89C4                 addiu   $s2, 1
    ROM:804A89C8                 andi    $s1, 0x1FFF
    ROM:804A89CC
    ROM:804A89CC loc_804A89CC:                            # CODE XREF: Lzpf_Expand+208↑j
    ROM:804A89CC                                          # Lzpf_Expand+25C↑j
    ROM:804A89CC                 lw      $v0, 0x10($s3)
    ROM:804A89D0
    ROM:804A89D0 loc_804A89D0:                            # CODE XREF: Lzpf_Expand:loc_804A8864↑j
    ROM:804A89D0                                          # Lzpf_Expand+2B8↑j
    ROM:804A89D0                 slti    $v0, 0x13
    ROM:804A89D4                 beqz    $v0, loc_804A88C8
    ROM:804A89D8                 srl     $v0, $s4, 11
    ROM:804A89DC                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A89E0
    ROM:804A89E0 loc_804A89E0:                            # CODE XREF: Lzpf_Expand+68↑j
    ROM:804A89E0                 li      $v1, 0xFFFFFFFF
    ROM:804A89E4                 addiu   $v0, -1
    ROM:804A89E8                 bne     $v0, $v1, loc_804A8890
    ROM:804A89EC                 sw      $v0, 0x38+arg_8($sp)
    ROM:804A89F0
    ROM:804A89F0 loc_804A89F0:                            # CODE XREF: Lzpf_Expand+1D0↑j
    ROM:804A89F0                 sw      $s1, 0x44($s3)
    ROM:804A89F4
    ROM:804A89F4 loc_804A89F4:                            # CODE XREF: Lzpf_Expand:loc_804A887C↑j
    ROM:804A89F4                 sw      $s4, 0x3C($s3)
    ROM:804A89F8                 j       loc_804A8A98
    ROM:804A89FC                 sh      $s5, 0x1C($s3)
    ROM:804A8A00  # ---------------------------------------------------------------------------
    ROM:804A8A00
    ROM:804A8A00 loc_804A8A00:                            # CODE XREF: Lzpf_Expand:loc_804A8998↑j
    ROM:804A8A00                 li      $v0, 5
    ROM:804A8A04
    ROM:804A8A04 loc_804A8A04:                            # CODE XREF: Lzpf_Expand+140↑j
    ROM:804A8A04                 sw      $v0, 0x38($s3)
    ROM:804A8A08                 lw      $v0, 0x38+arg_8($sp)
    ROM:804A8A0C                 sw      $s1, 0x44($s3)
    ROM:804A8A10                 bgez    $v0, loc_804A8A20
    ROM:804A8A14                 sw      $s4, 0x3C($s3)
    ROM:804A8A18                 j       loc_804A8ACC
    ROM:804A8A1C                 li      $v0, 0xFFFFFFFF
    ROM:804A8A20  # ---------------------------------------------------------------------------
    ROM:804A8A20
    ROM:804A8A20 loc_804A8A20:                            # CODE XREF: Lzpf_Expand+358↑j
    ROM:804A8A20                 lw      $v0, 0x10($s3)
    ROM:804A8A24                 bltzl   $v0, loc_804A8A2C
    ROM:804A8A28                 addiu   $v0, 7
    ROM:804A8A2C
    ROM:804A8A2C loc_804A8A2C:                            # CODE XREF: Lzpf_Expand+36C↑j
    ROM:804A8A2C                 sra     $v0, 3
    ROM:804A8A30                 sw      $v0, 0x54($s3)
    ROM:804A8A34                 sh      $s5, 0x1C($s3)
    ROM:804A8A38                 move    $a0, $s3
    ROM:804A8A3C                 addiu   $a1, $sp, 0x38+arg_8
    ROM:804A8A40                 jal     CheckPartialChecksum
    ROM:804A8A44                 addiu   $a2, $sp, 0x38+arg_4
    ROM:804A8A48                 bgezl   $v0, loc_804A8A5C
    ROM:804A8A4C                 lw      $v0, 0x54($s3)
    ROM:804A8A50                 break   0
    ROM:804A8A54                 j       loc_804A8ACC
    ROM:804A8A58                 li      $v0, 0xFFFFFFFF
    ROM:804A8A5C  # ---------------------------------------------------------------------------
    ROM:804A8A5C
    ROM:804A8A5C loc_804A8A5C:                            # CODE XREF: Lzpf_Expand+390↑j
    ROM:804A8A5C                 lw      $v1, 0x38+arg_8($sp)
    ROM:804A8A60                 li      $a0, 3
    ROM:804A8A64                 addu    $v0, $v1
    ROM:804A8A68                 bne     $v0, $a0, loc_804A8A8C
    ROM:804A8A6C                 sw      $v0, 0x54($s3)
    ROM:804A8A70                 lw      $v1, 0x38($s3)
    ROM:804A8A74
    ROM:804A8A74 loc_804A8A74:                            # CODE XREF: Lzpf_Expand+C0↑j
    ROM:804A8A74                 li      $v0, 6
    ROM:804A8A78                 bne     $v1, $v0, loc_804A8ACC
    ROM:804A8A7C                 li      $v0, 0xFFFFFFFF
    ROM:804A8A80                 li      $v0, 7
    ROM:804A8A84                 j       loc_804A8A98
    ROM:804A8A88                 sw      $v0, 0x38($s3)
    ROM:804A8A8C  # ---------------------------------------------------------------------------
    ROM:804A8A8C
    ROM:804A8A8C loc_804A8A8C:                            # CODE XREF: Lzpf_Expand+B8↑j
    ROM:804A8A8C                                          # Lzpf_Expand+3B0↑j
    ROM:804A8A8C                 sltiu   $v0, 4
    ROM:804A8A90                 beqz    $v0, loc_804A8ACC
    ROM:804A8A94                 li      $v0, 0xFFFFFFFF
    ROM:804A8A98
    ROM:804A8A98 loc_804A8A98:                            # CODE XREF: Lzpf_Expand+340↑j
    ROM:804A8A98                                          # Lzpf_Expand+3CC↑j
    ROM:804A8A98                 lw      $v1, 0x38($s3)
    ROM:804A8A9C                 li      $v0, 7
    ROM:804A8AA0                 beql    $v1, $v0, loc_804A8AC8
    ROM:804A8AA4                 sb      $zero, 0x58($s3)
    ROM:804A8AA8                 beq     $s2, $s6, loc_804A8AC4
    ROM:804A8AAC                 li      $v0, 1
    ROM:804A8AB0                 addiu   $s2, -1
    ROM:804A8AB4                 lbu     $v1, 0($s2)
    ROM:804A8AB8                 sb      $v0, 0x58($s3)
    ROM:804A8ABC                 j       loc_804A8AC8
    ROM:804A8AC0                 sb      $v1, 0x59($s3)
    ROM:804A8AC4  # ---------------------------------------------------------------------------
    ROM:804A8AC4
    ROM:804A8AC4 loc_804A8AC4:                            # CODE XREF: Lzpf_Expand+3F0↑j
    ROM:804A8AC4                 sb      $zero, 0x58($s3)
    ROM:804A8AC8
    ROM:804A8AC8 loc_804A8AC8:                            # CODE XREF: Lzpf_Expand+3E8↑j
    ROM:804A8AC8                                          # Lzpf_Expand+404↑j
    ROM:804A8AC8                 subu    $v0, $s2, $s6
    ROM:804A8ACC
    ROM:804A8ACC loc_804A8ACC:                            # CODE XREF: Lzpf_Expand+34↑j
    ROM:804A8ACC                                          # Lzpf_Expand+A8↑j ...
    ROM:804A8ACC                 lw      $ra, 0x38+var_4($sp)
    ROM:804A8AD0                 lw      $s6, 0x38+var_8($sp)
    ROM:804A8AD4                 lw      $s5, 0x38+var_C($sp)
    ROM:804A8AD8                 lw      $s4, 0x38+var_10($sp)
    ROM:804A8ADC                 lw      $s3, 0x38+var_14($sp)
    ROM:804A8AE0                 lw      $s2, 0x38+var_18($sp)
    ROM:804A8AE4                 lw      $s1, 0x38+var_1C($sp)
    ROM:804A8AE8                 lw      $s0, 0x38+var_20($sp)
    ROM:804A8AEC                 jr      $ra
    ROM:804A8AF0                 addiu   $sp, 0x38
    ROM:804A8AF0  # End of function Lzpf_Expand
    """
    def Lzpf_Expand(self, compressed_data, reset = True):
        if reset:
            self.clear()

        uncompressed_data = bytearray()
        block = ctypes.c_uint32(0)
        flags = 0xFFFF

        compressed_len = len(compressed_data)

        for i in range(compressed_len):
            byte = ctypes.c_uint32(compressed_data[i]).value

            self.decode["current_data"].value = self.decode["current_data"].value | (byte << (0x18 - (self.decode["current_width"].value & 0x1f)))
            self.decode["current_width"].value = self.decode["current_width"].value + 8
                
            while self.decode["current_width"].value >= 0x13:
                if (self.decode["current_data"].value & 0x80000000) == 0x80000000 and flags != 0xFFFF:
                    match = self.ReadMatch()

                    _flags = flags

                    for ii in range(match):
                        matched_byte = uncompressed_data[_flags]
                        
                        uncompressed_data.append(matched_byte)

                        block.value = (block.value << 8) | matched_byte
                        _flags += 1
                else:
                    literal = 0

                    if flags == 0xFFFF:
                        literal = self.HuffDecodeLiteralNoFlags()
                    else:
                        literal = self.HuffDecodeLiteral()

                    if literal != None:
                        uncompressed_data.append(literal)

                        block.value = (block.value << 8) | literal
                    else:
                        return uncompressed_data

                if len(uncompressed_data) >= 3:
                    flags_index = ((block.value >> 0x0B) ^ block.value) & 0xFFF
                    flags = self.decode["flags_table"][flags_index] 

                    self.decode["flags_table"][flags_index] = len(uncompressed_data)

                    if len(uncompressed_data) == 3:
                        break



        return uncompressed_data

    """
    ROM:804A84C8 ReadMatch:                               # CODE XREF: Lzpf_Expand+248↓p
    ROM:804A84C8                 lw      $a3, 0xC($a0)
    ROM:804A84CC                 lui     $v1, 0x806D
    ROM:804A84D0                 srl     $v0, $a3, 25
    ROM:804A84D4                 andi    $t0, $v0, 0x3E
    ROM:804A84D8                 la      $v1, dword_806D454C
    ROM:804A84DC                 addiu   $v0, $t0, 1
    ROM:804A84E0                 addu    $v0, $v1
    ROM:804A84E4                 lbu     $a1, 0($v0)
    ROM:804A84E8                 beqz    $a1, loc_804A84FC
    ROM:804A84EC                 addu    $v0, $t0, $v1
    ROM:804A84F0                 lbu     $v0, 0($v0)
    ROM:804A84F4                 j       loc_804A8530
    ROM:804A84F8                 sw      $v0, 0($a2)
    ROM:804A84FC  # ---------------------------------------------------------------------------
    ROM:804A84FC
    ROM:804A84FC loc_804A84FC:                            # CODE XREF: ReadMatch+20↑j
    ROM:804A84FC                 lui     $v0, 0x3E0
    ROM:804A8500                 and     $v1, $a3, $v0
    ROM:804A8504                 beq     $v1, $v0, loc_804A851C
    ROM:804A8508                 li      $a1, 0xB
    ROM:804A850C                 srl     $v0, $v1, 21
    ROM:804A8510                 addiu   $v0, 0xB
    ROM:804A8514                 j       loc_804A8530
    ROM:804A8518                 sw      $v0, 0($a2)
    ROM:804A851C  # ---------------------------------------------------------------------------
    ROM:804A851C
    ROM:804A851C loc_804A851C:                            # CODE XREF: ReadMatch+3C↑j
    ROM:804A851C                 srl     $v0, $a3, 13
    ROM:804A8520                 andi    $v0, 0xFF
    ROM:804A8524                 addiu   $v0, 0x2A
    ROM:804A8528                 sw      $v0, 0($a2)
    ROM:804A852C                 li      $a1, 0x13
    ROM:804A8530
    ROM:804A8530 loc_804A8530:                            # CODE XREF: ReadMatch+2C↑j
    ROM:804A8530                                          # ReadMatch+4C↑j
    ROM:804A8530                 lw      $v0, 0x10($a0)
    ROM:804A8534                 lw      $v1, 0xC($a0)
    ROM:804A8538                 subu    $v0, $a1
    ROM:804A853C                 sllv    $v1, $a1
    ROM:804A8540                 sw      $v0, 0x10($a0)
    ROM:804A8544                 sw      $v1, 0xC($a0)
    ROM:804A8548                 jr      $ra
    ROM:804A854C                 move    $v0, $zero
    ROM:804A854C  # End of function ReadMatch
    """
    def ReadMatch(self):
        match = 0

        width_index = (self.decode["current_data"].value >> 0x19) & 0x3E

        data_width = self.decode["code_widths"][1][width_index + 1]
        if data_width == 0:
            if (self.decode["current_data"].value & 0x3e00000) == 0x3e00000:
                match = ((self.decode["current_data"].value >> 0x0D) & 0xFF) + 0x2A
                data_width = 0x13
            else:
                match = ((self.decode["current_data"].value & 0x3e00000) >> 0x15) + 0x0B
                data_width = 0x0B
        else:
            match = self.decode["code_widths"][1][width_index]

        self.decode["current_data"].value <<= (data_width & 0x1F)
        self.decode["current_width"].value -= data_width

        return match

    """
    ROM:804A83C8 HuffDecodeLiteralNoFlags:                # CODE XREF: Lzpf_Expand+134↓p
    ROM:804A83C8                                          # Lzpf_Expand+2D4↓p
    ROM:804A83C8                 move    $t1, $a0
    ROM:804A83CC                 lw      $t0, 0xC($t1)
    ROM:804A83D0                 la      $v1, dword_806D434C
    ROM:804A83D8                 srl     $v0, $t0, 23
    ROM:804A83DC                 addu    $v0, $v1
    ROM:804A83E0                 lbu     $a1, 0($v0)
    ROM:804A83E4                 blez    $a1, loc_804A8424
    ROM:804A83E8                 lui     $v1, 0x806D
    ROM:804A83EC                 la      $v1, dword_806D41A0
    ROM:804A83F0                 sll     $v0, $a1, 2
    ROM:804A83F4                 addu    $v0, $v1
    ROM:804A83F8                 lw      $a0, 0($v0)
    ROM:804A83FC                 lw      $v0, 0x10($t1)
    ROM:804A8400                 and     $a3, $t0, $a0
    ROM:804A8404                 li      $v1, 0x20
    ROM:804A8408                 sllv    $a0, $t0, $a1
    ROM:804A840C                 subu    $v0, $a1
    ROM:804A8410                 subu    $v1, $a1
    ROM:804A8414                 sw      $v0, 0x10($t1)
    ROM:804A8418                 sw      $a0, 0xC($t1)
    ROM:804A841C                 j       loc_804A847C
    ROM:804A8420                 srlv    $a3, $v1
    ROM:804A8424  # ---------------------------------------------------------------------------
    ROM:804A8424
    ROM:804A8424 loc_804A8424:                            # CODE XREF: HuffDecodeLiteralNoFlags+1C↑j
    ROM:804A8424                 lui     $v0, 0x806D
    ROM:804A8428                 addiu   $a0, $v0, (dword_806D4324 - 0x806D0000)
    ROM:804A842C                 lbu     $v0, (byte_806D432E - 0x806D4324)($a0)
    ROM:804A8430                 srl     $a3, $t0, 22
    ROM:804A8434                 sltu    $v0, $a3, $v0
    ROM:804A8438                 beqz    $v0, loc_804A8464
    ROM:804A843C                 li      $a1, 0xA
    ROM:804A8440                 addiu   $a1, 1
    ROM:804A8444
    ROM:804A8444 loc_804A8444:                            # CODE XREF: HuffDecodeLiteralNoFlags+94↓j
    ROM:804A8444                 li      $v0, 0x20
    ROM:804A8448                 addu    $v1, $a1, $a0
    ROM:804A844C                 subu    $v0, $a1
    ROM:804A8450                 lbu     $v1, 0($v1)
    ROM:804A8454                 srlv    $a3, $t0, $v0
    ROM:804A8458                 sltu    $v1, $a3, $v1
    ROM:804A845C                 bnezl   $v1, loc_804A8444
    ROM:804A8460                 addiu   $a1, 1
    ROM:804A8464
    ROM:804A8464 loc_804A8464:                            # CODE XREF: HuffDecodeLiteralNoFlags+70↑j
    ROM:804A8464                 lw      $v1, 0xC($t1)
    ROM:804A8468                 lw      $v0, 0x10($t1)
    ROM:804A846C                 sllv    $v1, $a1
    ROM:804A8470                 subu    $v0, $a1
    ROM:804A8474                 sw      $v0, 0x10($t1)
    ROM:804A8478                 sw      $v1, 0xC($t1)
    ROM:804A847C
    ROM:804A847C loc_804A847C:                            # CODE XREF: HuffDecodeLiteralNoFlags+54↑j
    ROM:804A847C                 li      $v0, 0x99
    ROM:804A8480                 bne     $a3, $v0, loc_804A849C
    ROM:804A8484                 lui     $v0, 0x806D
    ROM:804A8488                 li      $v0, 0x10
    ROM:804A848C                 bne     $a1, $v0, loc_804A849C
    ROM:804A8490                 lui     $v0, 0x806D
    ROM:804A8494                 jr      $ra
    ROM:804A8498                 li      $v0, 0xFFFFFFFE
    ROM:804A849C  # ---------------------------------------------------------------------------
    ROM:804A849C
    ROM:804A849C loc_804A849C:                            # CODE XREF: HuffDecodeLiteralNoFlags+B8↑j
    ROM:804A849C                                          # HuffDecodeLiteralNoFlags+C4↑j
    ROM:804A849C                 addiu   $v0, (dword_806D4338 - 0x806D0000)
    ROM:804A84A0                 addu    $v0, $a1, $v0
    ROM:804A84A4                 lb      $v1, 0($v0)
    ROM:804A84A8                 la      $v0, unk_806D4224
    ROM:804A84B0                 addu    $v1, $a3, $v1
    ROM:804A84B4                 addu    $v1, $v0
    ROM:804A84B8                 lbu     $v1, 0($v1)
    ROM:804A84BC                 move    $v0, $zero
    ROM:804A84C0                 jr      $ra
    ROM:804A84C4                 sb      $v1, 0($a2)
    ROM:804A84C4  # End of function HuffDecodeLiteralNoFlags
    """
    def HuffDecodeLiteralNoFlags(self):
        code = 0

        data_width = self.decode["code_widths"][0][self.decode["current_data"].value >> 0x17]

        if data_width == 0:
            code = self.decode["current_data"].value >> 0x16

            data_width = 0x0A
            
            if code < self.decode["codes"][2][3]:
                while True:
                    data_width += 1

                    code = self.decode["current_data"].value >> (0x20 - (data_width & 0x1F))

                    if code >= self.decode["codes"][2][data_width]:
                        break
        else:
            code = (self.decode["current_data"].value & self.decode["codes"][0][data_width]) >> (0x20 - (data_width & 0x1F))

        self.decode["current_data"].value <<= (data_width & 0x1F)
        self.decode["current_width"].value -= data_width

        if code == 0x99 and data_width == 0x10:
            return None
        else:
            return self.decode["codes"][1][(code + ctypes.c_byte(self.decode["codes"][3][data_width]).value)]

    """
    ROM:804A82C0 HuffDecodeLiteral:                       # CODE XREF: Lzpf_Expand:loc_804A8978↓p
    ROM:804A82C0                 move    $t1, $a0
    ROM:804A82C4                 lw      $t0, 0xC($t1)
    ROM:804A82C8                 la      $v1, dword_806D434C
    ROM:804A82D0                 srl     $v0, $t0, 22
    ROM:804A82D4                 addu    $v0, $v1
    ROM:804A82D8                 lbu     $a3, 0($v0)
    ROM:804A82DC                 blez    $a3, loc_804A8320
    ROM:804A82E0                 addiu   $a0, $a3, 1
    ROM:804A82E4                 la      $v1, dword_806D41A0
    ROM:804A82EC                 sll     $v0, $a0, 2
    ROM:804A82F0                 addu    $v0, $v1
    ROM:804A82F4                 lw      $a1, 0($v0)
    ROM:804A82F8                 lw      $v0, 0x10($t1)
    ROM:804A82FC                 li      $v1, 0x1F
    ROM:804A8300                 subu    $v0, $a0
    ROM:804A8304                 and     $a1, $t0, $a1
    ROM:804A8308                 sllv    $a0, $t0, $a0
    ROM:804A830C                 subu    $v1, $a3
    ROM:804A8310                 sw      $v0, 0x10($t1)
    ROM:804A8314                 sw      $a0, 0xC($t1)
    ROM:804A8318                 j       loc_804A837C
    ROM:804A831C                 srlv    $a1, $v1
    ROM:804A8320  # ---------------------------------------------------------------------------
    ROM:804A8320
    ROM:804A8320 loc_804A8320:                            # CODE XREF: HuffDecodeLiteral+1C↑j
    ROM:804A8320                 lui     $v0, 0x806D
    ROM:804A8324                 addiu   $a0, $v0, (dword_806D4324 - 0x806D0000)
    ROM:804A8328                 lbu     $v0, (byte_806D432E - 0x806D4324)($a0)
    ROM:804A832C                 srl     $a1, $t0, 21
    ROM:804A8330                 sltu    $v0, $a1, $v0
    ROM:804A8334                 beqz    $v0, loc_804A8360
    ROM:804A8338                 li      $a3, 0xA
    ROM:804A833C                 addiu   $a3, 1
    ROM:804A8340
    ROM:804A8340 loc_804A8340:                            # CODE XREF: HuffDecodeLiteral+98↓j
    ROM:804A8340                 li      $v0, 0x1F
    ROM:804A8344                 addu    $v1, $a3, $a0
    ROM:804A8348                 subu    $v0, $a3
    ROM:804A834C                 lbu     $v1, 0($v1)
    ROM:804A8350                 srlv    $a1, $t0, $v0
    ROM:804A8354                 sltu    $v1, $a1, $v1
    ROM:804A8358                 bnezl   $v1, loc_804A8340
    ROM:804A835C                 addiu   $a3, 1
    ROM:804A8360
    ROM:804A8360 loc_804A8360:                            # CODE XREF: HuffDecodeLiteral+74↑j
    ROM:804A8360                 lw      $v0, 0xC($t1)
    ROM:804A8364                 lw      $v1, 0x10($t1)
    ROM:804A8368                 addiu   $a0, $a3, 1
    ROM:804A836C                 subu    $v1, $a0
    ROM:804A8370                 sllv    $v0, $a0
    ROM:804A8374                 sw      $v1, 0x10($t1)
    ROM:804A8378                 sw      $v0, 0xC($t1)
    ROM:804A837C
    ROM:804A837C loc_804A837C:                            # CODE XREF: HuffDecodeLiteral+58↑j
    ROM:804A837C                 li      $v0, 0x99
    ROM:804A8380                 bne     $a1, $v0, loc_804A839C
    ROM:804A8384                 lui     $v0, 0x806D
    ROM:804A8388                 li      $v0, 0x10
    ROM:804A838C                 bne     $a3, $v0, loc_804A839C
    ROM:804A8390                 lui     $v0, 0x806D
    ROM:804A8394                 jr      $ra
    ROM:804A8398                 li      $v0, 0xFFFFFFFE
    ROM:804A839C  # ---------------------------------------------------------------------------
    ROM:804A839C
    ROM:804A839C loc_804A839C:                            # CODE XREF: HuffDecodeLiteral+C0↑j
    ROM:804A839C                                          # HuffDecodeLiteral+CC↑j
    ROM:804A839C                 addiu   $v0, (dword_806D4338 - 0x806D0000)
    ROM:804A83A0                 addu    $v0, $a3, $v0
    ROM:804A83A4                 lb      $v1, 0($v0)
    ROM:804A83A8                 la      $v0, unk_806D4224
    ROM:804A83B0                 addu    $v1, $a1, $v1
    ROM:804A83B4                 addu    $v1, $v0
    ROM:804A83B8                 lbu     $v1, 0($v1)
    ROM:804A83BC                 move    $v0, $zero
    ROM:804A83C0                 jr      $ra
    ROM:804A83C4                 sb      $v1, 0($a2)
    ROM:804A83C4  # End of function HuffDecodeLiteral
    """
    def HuffDecodeLiteral(self):
        code = 0

        data_width = self.decode["code_widths"][0][self.decode["current_data"].value >> 0x16]

        if data_width == 0:
            code = self.decode["current_data"].value >> 0x15
            data_width = 0x0A

            if code < self.decode["codes"][2][3]:
                while True:
                    data_width += 1

                    code = self.decode["current_data"].value >> (0x1F - (data_width & 0x1F))

                    if code >= self.decode["codes"][2][data_width]:
                        break
        else:
            code = (self.decode["current_data"].value & self.decode["codes"][0][(data_width + 1)]) >> (0x1F - (data_width & 0x1F))

        self.decode["current_data"].value <<= ((data_width + 1) & 0x1F)
        self.decode["current_width"].value -= (data_width + 1)

        if code == 0x99 and data_width == 0x10:
            return None
        else:
            return self.decode["codes"][1][(code + ctypes.c_byte(self.decode["codes"][3][data_width]).value)]
