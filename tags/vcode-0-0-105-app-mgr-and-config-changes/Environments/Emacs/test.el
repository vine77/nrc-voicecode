
(setq debug-on-error t)
(setq debug-on-quit t)
;(c-toggle-auto-state nil)

(setq vr-activation-list (list "\.py$" "\.c$" "\.cpp$" "\.h$"))
(message "**-- test.el: debug-on-error=%S\n" debug-on-error)
(vr-mode 1 "vcode")

;;; Somehow if this is uncommented, the debugger doesn't kick in 
;;; even if I invoke (debug) explicitly inside vr-output-filter
;(setq debug-on-error nil)
;(setq debug-on-quit nil)
