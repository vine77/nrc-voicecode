(defun close-all-buffers ()
   (interactive)
   (let ((all-buffs (buffer-list)) (curr-buffer))
     (while all-buffs
       (setq curr-buffer (car all-buffs))
       (message "-- curr-buffer=%S, (buffer-name curr-buffer)=%S" curr-buffer (buffer-name curr-buffer))
       (setq all-buffs (cdr all-buffs))
       (kill-buffer curr-buffer)
     )
   )
)

(setq debug-on-error t)
(setq debug-on-quit t)

(close-all-buffers)

;(setq vr-activation-list (list "\.py$" "\.c$" "\.cpp$" "\.h$"))
;(vr-mode 1 "vcode-test")

;;; Somehow if this is uncommented, the debugger doesn't kick in 
;;; even if I invoke (debug) explicitly inside vr-output-filter
;(setq debug-on-error nil)
;(setq debug-on-quit nil)


