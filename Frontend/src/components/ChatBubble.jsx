export default function ChatBubble({ message, isUser }) {
  return (
    <div className={`flex gap-3 mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center flex-shrink-0 shadow-md">
          <span className="text-white text-xs font-bold">AI</span>
        </div>
      )}
      <div className={isUser ? "message-user" : "message-bot"}>
        <p className="break-words whitespace-pre-wrap">{message}</p>
      </div>
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-secondary-300 to-secondary-400 flex-shrink-0 shadow-md" />
      )}
    </div>
  )
}
