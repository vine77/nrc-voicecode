;;;
;;; Macros for quickly moving to various directories of VoiceCode
;;;

(defun vcmed ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Mediator"))
)

(defun vcadm ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Admin"))
)

(defun vcdat ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data"))
)

(defun vctdat ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data/TestData"))
)

(defun vcbench ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data/TestData/Benchmark"))
)

(defun vcconf ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Config"))
)


