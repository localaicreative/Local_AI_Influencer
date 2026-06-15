#!/bin/bash
# Produktivitäts-Tracking für Local AI Influencer
# Usage: ./scripts/track.sh [status|start|end]

REPO_DIR="/home/bobadmin/projects/Local_AI_Influencer"
TRACK_FILE="$REPO_DIR/docs/tracking.log"

cd "$REPO_DIR" || exit 1

case "${1:-status}" in
  status)
    echo "=== Local AI Influencer — Produktivitäts-Status ==="
    echo ""
    
    # Git Stats
    TOTAL_COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo 0)
    FILES_COUNT=$(find . -not -path './.git/*' -type f | wc -l)
    LINES_ADDED=$(git log --numstat --format="" HEAD 2>/dev/null | awk '{s+=$1} END {print s+0}')
    
    echo "📊 Git Stats:"
    echo "   Commits: $TOTAL_COMMITS"
    echo "   Dateien: $FILES_COUNT"
    echo "   Zeilen hinzugefügt: $LINES_ADDED"
    echo ""
    
    # Letzte Commits
    echo "🕐 Letzte 5 Commits:"
    git log --oneline -5 2>/dev/null | sed 's/^/   /'
    echo ""
    
    # Projekte
    PROJECTS=$(find docs/ -name "*.md" -not -name "philosophie.md" -not -name "productivity-tracking.md" -not -name "tracking.log" 2>/dev/null | wc -l)
    CONTENT=$(find content/ -name "*.md" 2>/dev/null | wc -l)
    
    echo "📁 Content:"
    echo "   Projekt-Dokumente: $PROJECTS"
    echo "   Content-Dateien: $CONTENT"
    echo ""
    
    # Session-Log aus GOAL.md
    if [ -f "GOAL.md" ]; then
      echo "📝 Session-Log (aus GOAL.md):"
      grep -A 100 "^| Datum |" GOAL.md 2>/dev/null | tail -n +3 | grep "|" | head -5 | sed 's/^/   /'
    fi
    ;;
    
  start)
    SESSION="$2"
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    echo "$TIMESTAMP | START | $SESSION" >> "$TRACK_FILE"
    echo "✅ Session gestartet: '$SESSION'"
    echo "   Track-File: $TRACK_FILE"
    ;;
    
  end)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
    echo "$TIMESTAMP | END | $(tail -1 "$TRACK_FILE" 2>/dev/null | cut -d'|' -f3 | xargs)" >> "$TRACK_FILE"
    echo "✅ Session beendet: $TIMESTAMP"
    
    # Stats zeigen
    TOTAL_SESSIONS=$(grep -c "| START |" "$TRACK_FILE" 2>/dev/null || echo 0)
    echo "   Gesamte Sessions: $TOTAL_SESSIONS"
    ;;
    
  *)
    echo "Usage: $0 [status|start 'Beschreibung'|end]"
    ;;
esac
