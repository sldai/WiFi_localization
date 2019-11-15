
(cl:in-package :asdf)

(defsystem "rosaria-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "BumperState" :depends-on ("_package_BumperState"))
    (:file "_package_BumperState" :depends-on ("_package"))
  ))