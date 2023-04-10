
; =============== ;
;  FILAMENT SWAP  ;
; =============== ;

G91              ; Relative positioning

G1 Z5            ; Move head up
G1 E-50 F5000    ; Dump the filament out

G90              ; Absolute positioning

G1 X0 Y0 F5000   ; Move over to the side
M0               ; Pause

G91              ; Relative positioning

G1 E100 F250      ; Purge old filament
G1 Z-5           ; Move head down

G90              ; Absolute positioning

; ================ ;
;  CONTINUE PRINT  ;
; ================ ;